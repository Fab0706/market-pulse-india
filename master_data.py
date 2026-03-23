import os
import pandas as pd
import yfinance as yf
from fredapi import Fred
from dotenv import load_dotenv

# Load key
load_dotenv()
fred = Fred(api_key=os.getenv("FRED_API_KEY"))


# ── SECTION 2: FETCH MARKET INDICES ──

# Nifty 50
nifty = yf.download("^NSEI", period="1y")["Close"]
nifty.columns = ["Nifty50"]

# S&P 500
sp500 = yf.download("^GSPC", period="1y")["Close"]
sp500.columns = ["SP500"]

# USD/INR
usdinr = yf.download("USDINR=X", period="1y")["Close"]
usdinr.columns = ["USDINR"]


# US 10Y Bond Yield
us_bond = fred.get_series("DGS10", observation_start="2025-01-01")
us_bond.name = "US_Bond_Yield"

# India 10Y Bond Yield
india_bond = fred.get_series("INDIRLTLT01STM", observation_start="2025-01-01")
india_bond.name = "India_Bond_Yield"

# ── SECTION 3: FETCH INDIAN GIANTS ──
indian_tickers = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
    "HINDUNILVR.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "KOTAKBANK.NS",
    "LT.NS", "AXISBANK.NS", "ASIANPAINT.NS", "M&M.NS", "MARUTI.NS",
    "SUNPHARMA.NS", "WIPRO.NS", "ULTRACEMCO.NS", "NESTLEIND.NS", "POWERGRID.NS",
    "NTPC.NS", "ONGC.NS", "BAJFINANCE.NS", "HCLTECH.NS", "TITAN.NS"
]
indian_giants = yf.download(indian_tickers, period="1y")["Close"]

# ── SECTION 4: FETCH US GIANTS ──
us_tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA",
    "META", "BRK-B", "JPM", "JNJ", "XOM",
    "BAC", "WMT", "PG", "MA", "HD",
    "CVX", "ABBV", "MRK", "PFE", "KO",
    "PEP", "TSLA", "DIS", "NFLX", "BA"
]
us_giants = yf.download(us_tickers, period="1y")["Close"]


# ── SECTION 5: MERGE MARKET DATA ──

# Combine daily market data into one table
master_market = pd.concat([nifty, sp500, usdinr, us_bond], axis=1, sort=True)

# Add India bond yield - monthly so we forward fill missing days
master_market["India_Bond_Yield"] = india_bond.reindex(
    master_market.index, method="ffill"
)

# ── SECTION 6: CLEAN ALL DATASETS ──

# Drop rows where ALL values are missing
master_market = master_market.dropna(how="all")
indian_giants = indian_giants.dropna(how="all")
us_giants = us_giants.dropna(how="all")

# Forward fill remaining gaps
master_market = master_market.ffill()
indian_giants = indian_giants.ffill()
us_giants = us_giants.ffill()

# ── SECTION 7: SAVE TO CSV ──
master_market.to_csv("master_market.csv")
indian_giants.to_csv("master_indian_giants.csv")
us_giants.to_csv("master_us_giants.csv")

print("✅ master_market.csv saved!", master_market.shape)
print("✅ master_indian_giants.csv saved!", indian_giants.shape)
print("✅ master_us_giants.csv saved!", us_giants.shape)
print("\nMaster Market preview:")
print(master_market.tail())


# ── SECTION 8: LOAD UNICORN DATA ──
unicorns = pd.read_csv("unicorns.csv")
unicorns.to_csv("master_unicorns.csv", index=False)
print("✅ master_unicorns.csv saved!", unicorns.shape)