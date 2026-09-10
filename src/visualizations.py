import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import os
from datetime import date, timedelta


# =========================================================
# 1. DOWNLOAD TCS DATA
# =========================================================

ticker = "TCS.NS"

data = yf.download(
    ticker,
    start="2020-01-01",
    end=(date.today() + timedelta(days=1)).isoformat(),
    auto_adjust=False
)

data = data[["Close", "Volume"]].copy()

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

data.dropna(inplace=True)


# =========================================================
# 2. CALCULATE INDICATORS
# =========================================================

data["Daily_Return"] = data["Close"].pct_change()

data["MA_7"] = (
    data["Close"].rolling(7).mean()
)

data["MA_30"] = (
    data["Close"].rolling(30).mean()
)

data["EMA_12"] = (
    data["Close"].ewm(
        span=12,
        adjust=False
    ).mean()
)

data["EMA_26"] = (
    data["Close"].ewm(
        span=26,
        adjust=False
    ).mean()
)


# MACD

data["MACD"] = (
    data["EMA_12"] -
    data["EMA_26"]
)

data["MACD_Signal"] = (
    data["MACD"]
    .ewm(span=9, adjust=False)
    .mean()
)


# RSI

delta = data["Close"].diff()

gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss

data["RSI"] = (
    100 -
    (100 / (1 + rs))
)


# Volatility

data["Volatility"] = (
    data["Daily_Return"]
    .rolling(20)
    .std()
    * 100
)


data.dropna(inplace=True)


# =========================================================
# 3. CREATE OUTPUT FOLDER
# =========================================================

output_folder = "data/graphs"

os.makedirs(
    output_folder,
    exist_ok=True
)


# =========================================================
# 4. PRICE + MOVING AVERAGES
# =========================================================

plt.figure(figsize=(14, 7))

plt.plot(
    data.index,
    data["Close"],
    label="TCS Price"
)

plt.plot(
    data.index,
    data["MA_7"],
    label="7-Day Moving Average"
)

plt.plot(
    data.index,
    data["MA_30"],
    label="30-Day Moving Average"
)

plt.title(
    "TCS Stock Price and Moving Averages"
)

plt.xlabel("Date")
plt.ylabel("Price (₹)")

plt.legend()
plt.grid()

plt.tight_layout()

plt.savefig(
    f"{output_folder}/price_moving_averages.png"
)

plt.close()


# =========================================================
# 5. RSI
# =========================================================

plt.figure(figsize=(14, 5))

plt.plot(
    data.index,
    data["RSI"],
    label="RSI"
)

plt.axhline(
    70,
    linestyle="--",
    label="Overbought (70)"
)

plt.axhline(
    30,
    linestyle="--",
    label="Oversold (30)"
)

plt.title(
    "TCS Relative Strength Index (RSI)"
)

plt.xlabel("Date")
plt.ylabel("RSI")

plt.legend()
plt.grid()

plt.tight_layout()

plt.savefig(
    f"{output_folder}/rsi.png"
)

plt.close()


# =========================================================
# 6. MACD
# =========================================================

plt.figure(figsize=(14, 5))

plt.plot(
    data.index,
    data["MACD"],
    label="MACD"
)

plt.plot(
    data.index,
    data["MACD_Signal"],
    label="Signal"
)

plt.title(
    "TCS MACD Indicator"
)

plt.xlabel("Date")
plt.ylabel("MACD")

plt.legend()
plt.grid()

plt.tight_layout()

plt.savefig(
    f"{output_folder}/macd.png"
)

plt.close()


# =========================================================
# 7. VOLATILITY
# =========================================================

plt.figure(figsize=(14, 5))

plt.plot(
    data.index,
    data["Volatility"],
    label="20-Day Volatility"
)

plt.title(
    "TCS Rolling Volatility"
)

plt.xlabel("Date")
plt.ylabel("Volatility (%)")

plt.legend()
plt.grid()

plt.tight_layout()

plt.savefig(
    f"{output_folder}/volatility.png"
)
plt.show()

plt.close()


# =========================================================
# 8. VOLUME
# =========================================================

plt.figure(figsize=(14, 5))

plt.plot(
    data.index,
    data["Volume"],
    label="Trading Volume"
)

plt.title(
    "TCS Trading Volume"
)

plt.xlabel("Date")
plt.ylabel("Volume")

plt.legend()
plt.grid()

plt.tight_layout()

plt.savefig(
    f"{output_folder}/volume.png"
)

plt.close()


# =========================================================
# 9. SAVE PROCESSED DATA
# =========================================================

data.to_csv(
    "data/processed_market_data.csv"
)


# =========================================================
# 10. COMPLETE
# =========================================================

print("\n==========================================")
print("VISUALIZATION PIPELINE COMPLETE")
print("==========================================")

print("\nGenerated graphs:")

print(
    "✓ price_moving_averages.png"
)

print(
    "✓ rsi.png"
)

print(
    "✓ macd.png"
)

print(
    "✓ volatility.png"
)

print(
    "✓ volume.png"
)

print(
    "\nSaved to:",
    output_folder
)

print(
    "\nProcessed dataset:"
)

print(
    "data/processed_market_data.csv"
)

print("==========================================")