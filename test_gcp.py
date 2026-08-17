import os
from google.cloud import bigquery

# 1. Point Python to your secret digital passport file
# (Ensure 'gcp_key.json' matches the exact filename of the key in your folder!)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp_key.json"

try:
    print("Testing connection to Google Cloud Platform...")
    
    # 2. Initialize the BigQuery Client
    client = bigquery.Client()
    
    # 3. Request a list of active datasets in your project
    datasets = list(client.list_datasets())
    
    print("\n🎉 SUCCESS! Your computer is connected to Google Cloud!")
    print(f"Connected to GCP Project ID: {client.project}")
    print(f"Number of active datasets found: {len(datasets)}")

except Exception as e:
    print(f"\n❌ CONNECTION FAILED.")
    print(f"Error Details: {e}")
    print("\nTip: Double-check that your 'gcp_key.json' file is spelled correctly and inside this folder.")
