import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 1. Download data
ticker = "TCS.NS"

data = yf.download(
    ticker,
    start="2020-01-01",
    end="2026-01-01",
    auto_adjust=False
)

# 2. Keep only the important columns
data = data[["Close", "Volume"]].copy()

# 3. Remove missing values
data.dropna(inplace=True)

# 4. Daily percentage return
data["Daily_Return"] = data["Close"].pct_change() * 100

# 5. Moving averages
data["MA_7"] = data["Close"].rolling(window=7).mean()
data["MA_30"] = data["Close"].rolling(window=30).mean()

# 6. Daily volatility
data["Volatility_7"] = data["Daily_Return"].rolling(window=7).std()

# 7. Save processed data
data.to_csv("data/tcs_processed.csv")

# 8. Display results
print("\nProcessed Data:")
print(data.tail())

print("\nDataset Shape:", data.shape)

print("\nBasic Statistics:")
print(data[["Close", "Daily_Return", "MA_7", "MA_30", "Volatility_7"]].describe())

# 9. Plot stock price and moving averages
plt.figure(figsize=(12, 6))

plt.plot(data.index, data["Close"], label="Close Price")
plt.plot(data.index, data["MA_7"], label="7-Day MA")
plt.plot(data.index, data["MA_30"], label="30-Day MA")

plt.title("TCS Stock Price and Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (INR)")
plt.legend()
plt.grid()

plt.show()