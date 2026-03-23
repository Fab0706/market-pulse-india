import yfinance as yf

# 25 Indian Giants across all sectors
# .NS = National Stock Exchange of India
tickers = [
    "RELIANCE.NS",   # Energy & Retail
    "TCS.NS",        # IT
    "HDFCBANK.NS",   # Banking
    "INFY.NS",       # IT
    "ICICIBANK.NS",  # Banking
    "HINDUNILVR.NS", # FMCG
    "SBIN.NS",       # Banking
    "BHARTIARTL.NS", # Telecom
    "ITC.NS",        # FMCG
    "KOTAKBANK.NS",  # Banking
    "LT.NS",         # Infrastructure
    "AXISBANK.NS",   # Banking
    "ASIANPAINT.NS", # Paints
    "MARUTI.NS",     # Automobiles
    "M&M.NS",        # Automobiles
    "SUNPHARMA.NS",  # Pharma
    "WIPRO.NS",      # IT
    "ULTRACEMCO.NS", # Cement
    "NESTLEIND.NS",  # FMCG
    "POWERGRID.NS",  # Energy
    "NTPC.NS",       # Energy
    "ONGC.NS",       # Oil & Gas
    "BAJFINANCE.NS", # Finance
    "HCLTECH.NS",    # IT
    "TITAN.NS"       # Consumer Goods
]

# Download 1 year of closing prices for all 25 companies at once
indian_giants = yf.download(tickers, period="1y")["Close"]

# Show last 5 rows
print("Indian Giants - Last 5 days:")
print(indian_giants.tail())

# Show shape - how many rows and columns we have
print("\nDataset size:", indian_giants.shape)
