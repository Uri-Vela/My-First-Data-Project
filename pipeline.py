import pandas as pd
import psycopg2

# 1. Setup the connection parameters to PostgreSQL
db_config = {
    "dbname": "PowerPlantDB",         # Replace with your database name if different
    "user": "postgres",           # Your verified working username
    "password": "TGI@WRal2026*#",   # Replace with your actual local password
    "host": "localhost",
    "port": "5432"
}

try:
    # 2. Connect to the database
    conn = psycopg2.connect(**db_config)
    print("Successfully connected to PostgreSQL!")

    # 3. Pulling database tables metadata
    query = "SELECT* FROM steamproduction LIMIT 100;"

    # 4. Use Pandas to run the SQL and store it in a Python dataframe
    df = pd.read_sql_query(query, conn)

       # === START OF WEEK 2: DATA TRANSFORMATION ===
    print("Starting data transformation...")

    print("\n--- Original Data Preview ---")
    print(df.head()) 

    print("\n--- Missing Values Count ---")
    print(df.isnull().sum())

    # REAL TRANSFORMATION: Calculate the Pressure-to-Temperature Ratio
    print("\nCalculating pressure-to-temperature ratio column...")
    df['pressure_to_temp_ratio'] = df['steampressure'] / df['steamtemperature']
    
    # Round it to 4 decimal places so it stays clean
    df['pressure_to_temp_ratio'] = df['pressure_to_temp_ratio'].round(4)

    print("\nTransformation complete! New metrics column added successfully.")
    # === END OF WEEK 2: DATA TRANSFORMATION ===

    # 5. Export that transformed data out into a clean CSV file
    df.to_csv("extracted_data.csv", index=False)
    print("Data extracted successfully and saved to 'extracted_data.csv'!")

    # 6. Clean up and close the database connection
    conn.close()

except Exception as e:
    print(f"An error occurred: {e}")
