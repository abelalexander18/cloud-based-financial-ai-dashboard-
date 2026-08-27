import pandas as pd
import numpy as np
import yfinance as yf


# =========================================================
# 1. DOWNLOAD DATA
# =========================================================

ticker = "TCS.NS"

data = yf.download(
    ticker,
    start="2020-01-01",
    end="2026-08-18",
    auto_adjust=False
)

data = data[["Close", "Volume"]].copy()

# Handle yfinance MultiIndex
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

data.dropna(inplace=True)


# =========================================================
# 2. TECHNICAL INDICATORS
# =========================================================

# Daily return

data["Daily_Return"] = (
    data["Close"].pct_change()
)


# Moving averages

data["MA_7"] = (
    data["Close"].rolling(7).mean()
)

data["MA_30"] = (
    data["Close"].rolling(30).mean()
)


# EMA

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


# =========================================================
# 3. MACD
# =========================================================

data["MACD"] = (
    data["EMA_12"] - data["EMA_26"]
)

data["MACD_Signal"] = (
    data["MACD"]
    .ewm(
        span=9,
        adjust=False
    )
    .mean()
)

data["MACD_Histogram"] = (
    data["MACD"] -
    data["MACD_Signal"]
)


# =========================================================
# 4. RSI
# =========================================================

delta = data["Close"].diff()

gain = delta.clip(lower=0)

loss = -delta.clip(upper=0)

avg_gain = gain.rolling(14).mean()

avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss

data["RSI"] = (
    100 - (100 / (1 + rs))
)


# =========================================================
# 5. BOLLINGER BANDS
# =========================================================

data["BB_Middle"] = (
    data["Close"].rolling(20).mean()
)

bb_std = (
    data["Close"].rolling(20).std()
)

data["BB_Upper"] = (
    data["BB_Middle"] +
    2 * bb_std
)

data["BB_Lower"] = (
    data["BB_Middle"] -
    2 * bb_std
)


# =========================================================
# 6. VOLATILITY
# =========================================================

data["Volatility_7"] = (
    data["Daily_Return"]
    .rolling(7)
    .std()
)

data["Volatility_20"] = (
    data["Daily_Return"]
    .rolling(20)
    .std()
)


# =========================================================
# 7. MOMENTUM
# =========================================================

data["Momentum_7"] = (
    data["Close"].pct_change(7)
)

data["Momentum_30"] = (
    data["Close"].pct_change(30)
)


# =========================================================
# 8. VOLUME
# =========================================================

data["Volume_MA_20"] = (
    data["Volume"].rolling(20).mean()
)

data["Relative_Volume"] = (
    data["Volume"] /
    data["Volume_MA_20"]
)


# =========================================================
# 9. CLEAN DATA
# =========================================================

data.replace(
    [np.inf, -np.inf],
    np.nan,
    inplace=True
)

data.dropna(inplace=True)


# =========================================================
# 10. GET LATEST MARKET DATA
# =========================================================

latest = data.iloc[-1]


close = float(latest["Close"])

ma7 = float(latest["MA_7"])

ma30 = float(latest["MA_30"])

rsi = float(latest["RSI"])

macd = float(latest["MACD"])

macd_signal = float(
    latest["MACD_Signal"]
)

volatility = float(
    latest["Volatility_20"]
)

momentum7 = float(
    latest["Momentum_7"]
)

momentum30 = float(
    latest["Momentum_30"]
)

relative_volume = float(
    latest["Relative_Volume"]
)


# =========================================================
# 11. TREND SCORE
# =========================================================

trend_score = 0


# Price vs moving averages

if close > ma7:
    trend_score += 1
else:
    trend_score -= 1


if close > ma30:
    trend_score += 1
else:
    trend_score -= 1


# Short MA vs long MA

if ma7 > ma30:
    trend_score += 1
else:
    trend_score -= 1


# MACD

if macd > macd_signal:
    trend_score += 1
else:
    trend_score -= 1


# Momentum

if momentum7 > 0:
    trend_score += 1
else:
    trend_score -= 1


if momentum30 > 0:
    trend_score += 1
else:
    trend_score -= 1


# =========================================================
# 12. DETERMINE TREND
# =========================================================

if trend_score >= 4:

    trend = "BULLISH"

elif trend_score <= -4:

    trend = "BEARISH"

else:

    trend = "NEUTRAL"


# =========================================================
# 13. MOMENTUM CLASSIFICATION
# =========================================================

if momentum7 > 0.03 and momentum30 > 0.05:

    momentum_status = "STRONG POSITIVE"

elif momentum7 > 0 or momentum30 > 0:

    momentum_status = "MODERATE POSITIVE"

elif momentum7 < -0.03 and momentum30 < -0.05:

    momentum_status = "STRONG NEGATIVE"

else:

    momentum_status = "WEAK"


# =========================================================
# 14. RSI ANALYSIS
# =========================================================

if rsi >= 70:

    rsi_status = "OVERBOUGHT"

elif rsi <= 30:

    rsi_status = "OVERSOLD"

else:

    rsi_status = "NORMAL"


# =========================================================
# 15. VOLATILITY / RISK
# =========================================================

# Convert volatility to percentage

volatility_percent = volatility * 100


if volatility_percent < 1:

    volatility_status = "LOW"

elif volatility_percent < 2:

    volatility_status = "MEDIUM"

else:

    volatility_status = "HIGH"


# =========================================================
# 16. RISK SCORE
# =========================================================

risk_score = 50


# Volatility contribution

if volatility_percent >= 2:

    risk_score += 25

elif volatility_percent >= 1:

    risk_score += 10

else:

    risk_score -= 10


# RSI contribution

if rsi >= 70 or rsi <= 30:

    risk_score += 10


# Momentum contribution

if abs(momentum7) > 0.05:

    risk_score += 10


# Volume contribution

if relative_volume > 2:

    risk_score += 5


# Keep score between 0 and 100

risk_score = max(
    0,
    min(
        100,
        risk_score
    )
)


# =========================================================
# 17. RISK LEVEL
# =========================================================

if risk_score >= 70:

    risk_level = "HIGH"

elif risk_score >= 40:

    risk_level = "MEDIUM"

else:

    risk_level = "LOW"


# =========================================================
# 18. OVERALL MARKET SCORE
# =========================================================

market_score = 50 + (
    trend_score * 8
)

market_score = max(
    0,
    min(
        100,
        market_score
    )
)


# =========================================================
# 19. GENERATE INSIGHT
# =========================================================

if trend == "BULLISH":

    trend_message = (
        "TCS is showing positive technical momentum."
    )

elif trend == "BEARISH":

    trend_message = (
        "TCS is showing negative technical momentum."
    )

else:

    trend_message = (
        "TCS is showing mixed technical signals."
    )


if risk_level == "HIGH":

    risk_message = (
        "Market conditions indicate elevated risk "
        "and increased price uncertainty."
    )

elif risk_level == "MEDIUM":

    risk_message = (
        "Market conditions indicate moderate risk."
    )

else:

    risk_message = (
        "Market conditions indicate relatively low risk."
    )


insight = (
    trend_message + " "
    + risk_message
)


# =========================================================
# 20. DISPLAY RESULTS
# =========================================================

print("\n==========================================")
print("TCS AI FINANCIAL ANALYSIS")
print("==========================================")

print(
    f"Current Price : ₹{close:.2f}"
)

print(
    f"Trend Score   : {trend_score}"
)

print(
    f"Market Score  : {market_score:.0f}/100"
)

print(
    f"Trend         : {trend}"
)

print(
    f"Momentum      : {momentum_status}"
)

print(
    f"RSI           : {rsi:.2f}"
)

print(
    f"RSI Status    : {rsi_status}"
)

print(
    f"MACD          : {macd:.2f}"
)

print(
    f"MACD Signal   : {macd_signal:.2f}"
)

print(
    f"Volatility    : {volatility_percent:.2f}%"
)

print(
    f"Volatility    : {volatility_status}"
)

print(
    f"Relative Vol. : {relative_volume:.2f}x"
)

print(
    f"Risk Score    : {risk_score}/100"
)

print(
    f"Risk Level    : {risk_level}"
)

print("\nAI INSIGHT:")
print(insight)

print("==========================================")