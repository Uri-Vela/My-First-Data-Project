import pandas as pd
import psycopg2

# 1. Setup the connection parameters to PostgreSQL
db_config = {
    "dbname": "PowerPlantDB",
    "user": "postgres",
    "password": "TGI@WRal2026*#",
    "host": "localhost",
    "port": "5432"
}

try:
    # 2. Connect to the database
    conn = psycopg2.connect(**db_config)
    print("Successfully connected to PostgreSQL!")

    # 3. Write a simple SQL query to pull data (Change 'users' to a table that exists in your DB)
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"

    # 4. Use Pandas to run the SQL and store it in a Python dataframe (table)
    df = pd.read_sql_query(query, conn)

    # 5. Export that data out of the database and into a clean CSV file
    df.to_csv("extracted_data.csv", index=False)
    print("Data extracted successfully and saved to 'extracted_data.csv'!")

    # 6. Clean up and close the database connection
    conn.close()

except Exception as e:
    print(f"An error occurred: {e}")
