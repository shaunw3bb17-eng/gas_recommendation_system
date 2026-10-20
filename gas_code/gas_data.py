import sqlite3


def gas_history():

   conn = sqlite3.connect("gas_prices.db")  # Connect to the SQLite database.

   cursor = conn.cursor() # Create a cursor to execute SQL queries.

   cursor.execute("SELECT station, price, date FROM gas_prices")  # Retrieve the station name, price, and date for all records.

   rows = cursor.fetchall() # Fetch all records returned by the query.

   conn.close()  # Close the database connection after retrieving the data.

   return[   # Convert each database row into a dictionary for use in the application.
      {"name":row[0], "price":row[1],"date":row[2]} for row in rows
   ]
