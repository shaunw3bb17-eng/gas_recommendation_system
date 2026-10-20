import sqlite3


conn = sqlite3.connect("gas_prices.db") # Connect to the SQLite database, creating it if it does not exist.

cursor = conn.cursor() # Create a cursor to execute SQL statements.

# Create the gas_prices table if it has not already been created.
cursor.execute("""   
    CREATE TABLE IF NOT EXISTS gas_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    station TEXT,
    price REAL,
    date TEXT            
    )
""")
data = [  # Define sample fuel price records for each gas station.
             {"name":"Texaco", "price": 180,  "date": "2026-05-01"},
             {"name":"Texaco", "price": 182,  "date": "2026-05-08"},
             {"name":"Texaco", "price": 184,  "date": "2026-05-15"},
             {"name":"Texaco", "price": 186,  "date": "2026-05-22"},
         
             {"name":"Bonjour", "price": 181,  "date": "2026-05-01"},
             {"name":"Bonjour", "price": 183,  "date": "2026-05-08"},
             {"name":"Bonjour", "price": 185,  "date": "2026-05-15"},
             {"name":"Bonjour", "price": 187,  "date": "2026-05-22"},
        
             {"name":"Shibuya", "price": 187,  "date": "2026-05-01"},
             {"name":"Shibuya", "price": 189,  "date": "2026-05-08"},
             {"name":"Shibuya", "price": 191,  "date": "2026-05-15"},
             {"name":"Shibuya", "price": 193,  "date": "2026-05-22"},
        
             {"name":"Rubis", "price": 191,  "date": "2026-05-01"},
             {"name":"Rubis", "price": 193,  "date": "2026-05-08"},
             {"name":"Rubis", "price": 195,  "date": "2026-05-15"},
             {"name":"Rubis", "price": 197,  "date": "2026-05-22"}
]

rows = [(item["name"], item["price"], item["date"]) for item in data]  # Convert the dictionaries into tuples matching the database column order.

cursor.executemany(  # Insert all price records into the database using parameterized SQL.
    "INSERT INTO gas_prices(station,price, date)VALUES(?, ?, ?)",rows
)

conn.commit() # Save the database changes.
conn.close()  # Close the database connection when finished.

print("Data loaded!")  # Confirm that the data-loading script has completed.