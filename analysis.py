import pandas as pd
import numpy as np

# Load our clean master market data
master = pd.read_csv("master_market.csv", index_col=0, parse_dates=True)
# Quick check
print("Data loaded successfully!")
print("Shape:", master.shape)
print("\nFirst look:")
print(master.head())

# ── SECTION 2: CORRELATION MATRIX ──

# Calculate how strongly each market moves with every other market
correlation = master.corr()

print("\n── CORRELATION MATRIX ──")
print(correlation.round(2))

# ── SECTION 3: MOVING AVERAGES ── 

# 50-day moving average - shows short term trend
master["Nifty50_MA50"] = master["Nifty50"].rolling(window=50).mean()
master["SP500_MA50"] = master["SP500"].rolling(window=50).mean()

# 200-day moving average - shows long term trend
master["Nifty50_MA200"] = master["Nifty50"].rolling(window=200).mean()
master["SP500_MA200"] = master["SP500"].rolling(window=200).mean()

print("\n── MOVING AVERAGES ──")
print(master[["Nifty50", "Nifty50_MA50", "Nifty50_MA200"]].tail(10))

# ── SECTION 4: VOLATILITY ──

# 30-day rolling standard deviation shows how volatile each market is
master["Nifty50_Volatility"] = master["Nifty50"].rolling(window=30).std()
master["SP500_Volatility"] = master["SP500"].rolling(window=30).std()

print("\n── VOLATILITY (last 10 days) ──")
print(master[["Nifty50", "Nifty50_Volatility", "SP500", "SP500_Volatility"]].tail(10))

# ── SECTION 5: SAVE ANALYSIS RESULTS ──

# Save master data with all calculated columns
master.to_csv("master_analysis.csv")

print("\n── ANALYSIS COMPLETE ──")
print("✅ master_analysis.csv saved!", master.shape)
print("\nColumns saved:")
for col in master.columns:
    print(" -", col)
