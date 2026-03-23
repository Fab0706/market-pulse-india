#cd C:\Users\shana\OneDrive\Documents\Desktop\MPI
#venv\Scripts\activate


# This imports the yfinance library and gives it a short name 'yf'
import yfinance as yf

# Download 1 month of Nifty 50 data - ^NSEI is Nifty's ticker symbol
nifty = yf.download("^NSEI", period="1mo")

# Print the full data table to the terminal
print(nifty)