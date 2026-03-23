import os
from dotenv import load_dotenv
import pandas as pd
from fredapi import Fred

# Load the secret key from our .env file
load_dotenv()

# Connect to the FRED API using the key from the .env file
fred = Fred(api_key=os.getenv("FRED_API_KEY"))

# Download US 10-year bond yield data for last 1 year
bond_yield = fred.get_series("DGS10", observation_start="2023-01-01")

# print the bond yield data
print(bond_yield)