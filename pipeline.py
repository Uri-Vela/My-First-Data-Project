import pandas as pd
import psycopg2
import warnings

# Suppress the yellow Pandas connection warning to keep terminal clean
warnings.filterwarnings('ignore', category=UserWarning)

db_config = {
    "dbname": "PowerPlantDB",         # Ensure your DB name is correct
    "user": "postgres",           # Your verified username
    "password": "TGI@WRal2026*#",   # Replace with your actual working password
    "host": "localhost",
    "port": "5432"
}

try:
    conn = psycopg2.connect(**db_config)
    print("Successfully connected to PostgreSQL!")

    query = "SELECT * FROM steamproduction LIMIT 100;"
    df = pd.read_sql_query(query, conn)

    # === WEEK 2 TRANSFORMATION ===
    print("Starting data transformation...")
    df['pressure_to_temp_ratio'] = df['steampressure'] / df['steamtemperature']
    df['pressure_to_temp_ratio'] = df['pressure_to_temp_ratio'].round(4)
    print("Transformation complete! Metrics column added.")

    # === WEEK 3 DATA AGGREGATION ===
    print("\nStarting Week 3 Data Aggregation...")
    
    # Group telemetry data and compute the average
    summary_df = df.groupby('boilerid')[['steamtemperature', 'steampressure', 'pressure_to_temp_ratio']].mean()
    summary_df = summary_df.reset_index()
    summary_df = summary_df.round(2)
    
    summary_df = summary_df.rename(columns={
        'steamtemperature': 'avg_steam_temp',
        'steampressure': 'avg_steam_pressure',
        'pressure_to_temp_ratio': 'avg_pressure_temp_ratio'
    })

    print("\n--- Aggregated Summary Data Preview ---")
    print(summary_df)  # Crucial print command
    print("\nAggregation complete!")

    # === EXPORT DATA ===
    df.to_csv("extracted_data.csv", index=False)
    summary_df.to_csv("boiler_summary_report.csv", index=False)
    print("Both raw data and summary report saved successfully!")

    conn.close()

except Exception as e:
    print(f"An error occurred: {e}")
