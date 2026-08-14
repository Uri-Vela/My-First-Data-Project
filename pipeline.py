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
        # === START OF WEEK 4: CONDITIONAL AUTOMATION & ANOMALIES ===
    print("\nStarting Week 4 Automated Anomaly Detection...")
    
    # 1. Define safety thresholds
    MAX_SAFE_TEMP = 450.5
    anomalies_found = []

    # 2. Loop through each row of the summary report using Pandas .iterrows()
    for index, row in summary_df.iterrows():
        boiler = row['boilerid']
        current_avg_temp = row['avg_steam_temp']
        
        # 3. Conditional Check: Is the boiler running too hot?
        if current_avg_temp > MAX_SAFE_TEMP:
            alert_message = f"ALERT: Boiler ID {int(boiler)} is OVERHEATING! Avg Temp: {current_avg_temp}°C (Max Safe: {MAX_SAFE_TEMP}°C)"
            print(f"⚠️  {alert_message}")
            anomalies_found.append({"boilerid": int(boiler), "avg_temp": current_avg_temp, "status": "CRITICAL"})
        else:
            print(f"✅ Boiler ID {int(boiler)} is operating within normal safety limits.")

    # 4. Smart Automation: If anomalies exist, write an Emergency Alert File
    if len(anomalies_found) > 0:
        alert_df = pd.DataFrame(anomalies_found)
        alert_df.to_csv("emergency_alerts.log", index=False)
        print("\n[CRITICAL SUCCESS] Anomaly files generated! Check 'emergency_alerts.log' for details.")
    else:
        print("\n[SYSTEM HEALTHY] No thermal anomalies detected across any boiler networks.")
    # === END OF WEEK 4: CONDITIONAL AUTOMATION & ANOMALIES ===

    conn.close()

except Exception as e:
    print(f"An error occurred: {e}")
