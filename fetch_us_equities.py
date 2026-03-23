import yfinance as yf

# S&P 500 - US market index - complements Nifty 50
# ^GSPC is Yahoo Finance's ticker for the S&P 500
sp500 = yf.download("^GSPC", period="1y")["Close"]

print("S&P 500 closing prices:")
print(sp500.tail())