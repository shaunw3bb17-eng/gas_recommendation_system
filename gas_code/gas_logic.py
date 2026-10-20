from gas_data import gas_history
from station_location import stations
import math
from datetime import datetime
import os
import requests




API_KEY = os.getenv("TOMTOM_API_KEY") # API key used to access TomTom traffic data.

def gas_station_history(name):  # Return all recorded prices for the specified gas station.
    data = gas_history()
    return [x for x in data if x["name"].lower() == name.lower()]

def get_price(x):  # Extract the price from a gas station record.
    return x["price"]

def cheapest_gas():
    data = gas_history()

    latest = {}

    for item in data: # Keep only the most recent price record for each station.
        name = item["name"]

        if name not in latest:
            latest[name]= item
        else:
            if item["date"] > latest[name]["date"]:
                latest[name] = item

    return min(latest.values(), key = get_price)  # Return the station with the lowest current recorded price.


def price_trend(name):
    data = gas_history()
    prices = [x for x in data if x["name"].lower() == name.lower() ] # Filter the records to include only the selected station.

    if len(prices) < 2:  # A trend cannot be calculated with fewer than two price records.
        return {
            "name": name,
            "error":"insufficient prices"
        }
    
    prices.sort(key = lambda x:x["date"]) # Arrange prices chronologically before calculating changes.

    changes = []

    for i in range (1, len(prices)):  # Calculate the difference between each consecutive price record.
        change = prices[i]["price"] - prices[i-1]["price"]
        changes.append(change)
        
    avg_change = sum(changes) / len(changes) # Calculate the average price change across the recorded periods.

    
    if avg_change > 0: # Classify the overall trend according to the average change.
            trend = "increasing"
    elif avg_change < 0 :
        trend = "decreasing"
    else:
        trend = "constant"

    return {
        "name": name,
        "trend": trend,
        "average_weekly_change": avg_change
    }

def latest_price(name):
    data = gas_history()
    prices = [x for x in data if x["name"].lower() == name.lower()]

    if not prices: # Return None if the station has no recorded prices.
        return None
    
    latest = max(prices, key= lambda x:x["date"]) # Find and return the record with the most recent date.
    return latest


def average_price(name):
    data = gas_history()
    prices = [x for x in data if x["name"].lower() == name.lower()]

    if not prices:
        return None
    total = sum(x["price"] for x in prices) # Calculate the mean of all recorded prices for the station.

    return total / len(prices)


def volatile_change(name):
    data = gas_history()
    prices = [x for x in data if x["name"].lower() == name.lower()]

    if len(prices) < 2:  # Volatility requires at least two recorded prices for comparison.
        return {
            "name": name,
            "volatility": None,
            "issue": "insufficient values"
        } 
    

    prices.sort(key = lambda x:x["date"]) # Sort records by date to compare consecutive prices in order.

    changes = []

    for i in range (1, len(prices)): # Calculate the absolute change between consecutive prices.
        change = prices[i]["price"] - prices[i-1]["price"]
        changes.append(abs(change))
        
    return sum(changes) / len(changes)  # Return the average absolute price change.


def predicted_price(name):
    current = latest_price(name) # Retrieve the latest recorded price for the station.
    
    if not current:
        return None
    
    trend_val = price_trend(name) # Obtain the average price change to estimate the next price.
    
    next_price = current["price"] + trend_val["average_weekly_change"]
    
    return {
        "name": name,
        "current price": current["price"],
        "predicted_price" : next_price
    }

def station_report(name): # Gather the price information needed for the station report.
    trend_val = price_trend(name)
    current = latest_price(name)
    volatility = volatile_change(name)
    average = average_price(name)
    prediction = predicted_price(name)
    

    if "error" in trend_val: # Handle cases where there are insufficient records to calculate a trend.
        trend = None
        avg_change = None
    else:
        trend = trend_val["trend"]
        avg_change = trend_val["average_weekly_change"]


    return {   # Return a summary of the station's price history and prediction.
        "name": name,
        "current_price": current["price"] if current else None,
        "price_trend": trend,
        "average_price": average,
        "average_weekly_change": avg_change,
        "price_volatility": volatility,
        "next_predicted_price": prediction["predicted_price"] if prediction else None
    }


def every_station_profile():
    data = gas_history()

    names = set(x["name"] for x in data)  # Collect the unique station names from the available price records.

    return [station_report(name) for name in names]   # Generate a report for each station with recorded price data.



def best_station(user_lat, user_lon):
    ranked = ranked_stations(user_lat, user_lon)  # Rank available stations based on price, distance, and traffic.

    if not ranked: # Return an error if no eligible stations can be ranked.
        return {
            "error": "station not available."
        }
    best = ranked[0] # The first station has the lowest calculated recommendation score
    
    return {
        "best_station": best["station"]["name"],
        "address": best["station"]["address"],
        "current_price": best["price"],
        "distance_km": best["distance"],
        "traffic": best["traffic"],
        "score": best["score"]
    }

def ranked_stations(user_lat, user_lon):
    locations = stations()   # Retrieve the available station locations.
    candidates =[]

    for location in locations:
        current = latest_price(location["name"]) # Get the latest price for the station.
        if not current: # Skip stations without recorded prices.
            continue
 
        dist = distance(    # Calculate the distance from the user to the station.
            user_lat,user_lon, location["latitude"],location["longitude"]
        )
        traff = traffic(location["latitude"], location["longitude"]) # Estimate traffic congestion near the station.
        score = station_score(current["price"], dist, traff) # Calculate a combined score for comparing stations.

        candidates.append({ # Store the station details and its calculated values.
            "station": location,
            "price": current["price"],
            "distance": dist,
            "traffic": traff,
            "score": score
            })
    
    return sorted(candidates, key=lambda x:x["score"])  # Sort stations by score, placing the lowest-scoring station first.

    

def station_score(price,distance, traffic):
    return price + (distance * 0.7) + (traffic * 0.2)  # Combine price, distance, and traffic using their assigned weights.

def traffic(lat,lon):

    url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json" # TomTom endpoint for retrieving current traffic flow information.

    params = {  # Supply the station coordinates and API key to the request.
        "point":f"{lat},{lon}",
        "key": API_KEY
    }

    try:
        r = requests.get(url, params= params, timeout= 5)  # Request live traffic data with a five-second timeout.
        if r.status_code == 200:
            data = r.json()

            if "flowSegmentData" in data:   # Check that the response contains traffic flow information.
                flow = data["flowSegmentData"]

                current_speed = flow["currentSpeed"]  # Retrieve current and unrestricted road speeds.
                free_speed = flow["freeFlowSpeed"] 

                if free_speed > 0:

                    congestion = (1 - (current_speed / free_speed))* 100 # Estimate congestion as a percentage below free-flow speed.
                    return round(congestion, 2)
    except (requests.RequestException, KeyError, ValueError): # Continue to the fallback if the request or response cannot be processed.
        pass

    #temporary simulated data until able to get real data api 
    #used when live traffic not available

    hour = datetime.now().hour

    traffic_level = 20 # Use a default traffic level outside the specified peak periods.

    if 7 <= hour <= 9:  # Simulate heavier traffic during the morning rush hour.
        traffic_level = 60

    elif 16 <= hour <= 18: # Simulate heavier traffic during the evening rush hour.
        traffic_level = 70

    elif 22 <= hour or hour <= 5: # Simulate lighter traffic late at night and early in the morning.
        traffic_level = 10

    return traffic_level

def distance(lat1, lon1, lat2, lon2):
    R = 6371 # Earth's approximate radius in kilometres.

    dlat = math.radians(lat2 -lat1) # Convert coordinate differences from degrees to radians.
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) **2  # Apply the Haversine formula to calculate the central angle.
        + math.cos(math.radians(lat1)) 
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) **2
        )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c   # Return the approximate straight-line distance in kilometres.


def nearest_location(user_lat,user_lon):
    locations = stations() # Retrieve the available gas station locations.

    nearest= min(locations, key= lambda s: distance(user_lat,user_lon, s["latitude"], s["longitude"]))  # Find the station with the shortest distance from the user.

    return {
        "closest_station": nearest,
        "distance_km": distance(user_lat,user_lon,nearest["latitude"],nearest["longitude"])
    }

# Optional test code for checking the traffic function directly.
#if __name__ == "__main__":
    #result = traffic(18.04, -76.90)
    #print("Congestion:", result)






