import os
from dotenv import load_dotenv
import pandas as pd
from fredapi import Fred

# Load the secret key from our .env file
load_dotenv()

# Connect to the FRED API using the key from the .env file
fred = Fred(api_key=os.getenv("FRED_API_KEY"))

# Download India 10-year bond yield (monthly data from IMF)
india_bond = fred.get_series("INDIRLTLT01STM", observation_start="2025-01-01")

# print the bond yield data
print(india_bond)