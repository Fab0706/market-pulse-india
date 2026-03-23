import yfinance as yf

# 25 US Giants across all sectors
tickers = [
    "AAPL",  # Apple - Tech
    "MSFT",  # Microsoft - Tech
    "GOOGL", # Google - Tech
    "AMZN",  # Amazon - Retail/Cloud
    "NVDA",  # Nvidia - Semiconductors
    "META",  # Meta - Social Media
    "BRK-B", # Berkshire - Finance
    "JPM",   # JP Morgan - Banking
    "JNJ",   # Johnson & Johnson - Healthcare
    "XOM",   # Exxon - Oil & Gas
    "BAC",   # Bank of America - Banking
    "WMT",   # Walmart - Retail
    "PG",    # Procter & Gamble - FMCG
    "MA",    # Mastercard - Fintech
    "HD",    # Home Depot - Retail
    "CVX",   # Chevron - Oil & Gas
    "ABBV",  # AbbVie - Pharma
    "MRK",   # Merck - Pharma
    "PFE",   # Pfizer - Pharma
    "KO",    # Coca Cola - Beverages
    "PEP",   # Pepsi - Beverages
    "TSLA",  # Tesla - EV/Auto
    "DIS",   # Disney - Media
    "NFLX",  # Netflix - Streaming
    "BA"     # Boeing - Aerospace
]

# Download 1 year of closing prices
us_giants = yf.download(tickers, period="1y")["Close"]

print("US Giants - Last 5 days:")
print(us_giants.tail())

print("\nDataset size:", us_giants.shape)
