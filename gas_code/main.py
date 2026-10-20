from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware to allow the frontend to communicate with the backend.
from fastapi import FastAPI

# Import the functions used to retrieve and analyse gas station data.
from gas_logic import ( cheapest_gas, gas_station_history, price_trend, 
                        latest_price, station_report, every_station_profile, 
                        best_station, predicted_price, nearest_location, ranked_stations, traffic
)
from gas_data import gas_history  # Import the function that retrieves gas price history from the database.

app = FastAPI()  # Create the FastAPI application.

app.add_middleware(  # Configure CORS to allow requests from the local React development server.
    CORSMiddleware,
   allow_origins= ["http://localhost:5173"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"] 
)

@app.get("/gas_stations") # Return the available gas station price records.
def gas_stations():
    return gas_history()

@app.get("/cheapest_station") # Return the station with the lowest latest recorded gas price.
def get_cheapest():
    return cheapest_gas()

@app.get("/gas_prices/{name}") # Return the price history for a specified gas station.
def get_history(name: str):
    return gas_station_history(name)

@app.get("/price_trend/{name}")  # Return the price trend for a specified gas station.
def get_trend(name:str):
    return price_trend(name)

@app.get("/current_price/{name}") # Return the latest recorded price for a specified gas station.
def get_latest(name:str):
    return latest_price(name)

@app.get("/station_report/{name}")  # Return a report containing price statistics and predictions for a station.
def get_report(name:str):
    return station_report(name)

@app.get("/station_profiles")  # Return profiles containing price information for all recorded stations.
def get_all_station_profiles():
    return every_station_profile()

@app.get("/best_station")  # Recommend the best station based on the user's latitude and longitude.
def get_best_station(lat:float, lon:float):
    return best_station(lat, lon)

@app.get("/stations_ranked") # Return stations ranked by their recommendation scores for the user's location.
def get_stations_ranked(lat:float, lon:float):
    return ranked_stations(lat,lon)

@app.get("/next_price_prediction/{name}")  # Estimate the next fuel price for a specified gas station.
def get_next_prediction(name:str):
    return predicted_price(name)

@app.get("/nearest_station") # Find the gas station closest to the user's coordinates.
def get_nearest(lat:float,lon:float):
    return nearest_location(lat,lon)


@app.get("/")  # Provide basic information about the API when the root URL is accessed.

def root():
    return {
            "name" : "gas prediction server",
            "status" : "active",
            "docs" : "/docs"
            }

