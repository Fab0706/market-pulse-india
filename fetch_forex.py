import yfinance as yf

# Download 1 year of USD/INR exchange rate data - "USDINR=X" is the ticker symbol for USD/INR exchange rate
usd_inr = yf.download("USDINR=X", period="1y")

# Took only the closing price
usd_inr = usd_inr[["Close"]]

print(usd_inr)