import pandas as pd
import numpy as np
import yfinance as yf


# =========================================================
# 1. DOWNLOAD TCS DATA
# =========================================================

ticker = "TCS.NS"

data = yf.download(
    ticker,
    start="2020-01-01",
    end="2026-08-18",
    auto_adjust=False
)

data = data[["Close", "Volume"]].copy()

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

data.dropna(inplace=True)


# =========================================================
# 2. TECHNICAL INDICATORS
# =========================================================

data["Daily_Return"] = data["Close"].pct_change()

data["MA_7"] = data["Close"].rolling(7).mean()
data["MA_30"] = data["Close"].rolling(30).mean()

data["EMA_12"] = data["Close"].ewm(
    span=12,
    adjust=False
).mean()

data["EMA_26"] = data["Close"].ewm(
    span=26,
    adjust=False
).mean()


# MACD

data["MACD"] = (
    data["EMA_12"] - data["EMA_26"]
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

data["RSI"] = 100 - (
    100 / (1 + rs)
)


# Volatility

data["Volatility_20"] = (
    data["Daily_Return"]
    .rolling(20)
    .std()
)


# Momentum

data["Momentum_7"] = (
    data["Close"].pct_change(7)
)

data["Momentum_30"] = (
    data["Close"].pct_change(30)
)


# Volume

data["Volume_MA_20"] = (
    data["Volume"].rolling(20).mean()
)

data["Relative_Volume"] = (
    data["Volume"] /
    data["Volume_MA_20"]
)


# =========================================================
# 3. CLEAN DATA
# =========================================================

data.replace(
    [np.inf, -np.inf],
    np.nan,
    inplace=True
)

data.dropna(inplace=True)


# =========================================================
# 4. GET LATEST VALUES
# =========================================================

latest = data.iloc[-1]

close = float(latest["Close"])

ma7 = float(latest["MA_7"])
ma30 = float(latest["MA_30"])

rsi = float(latest["RSI"])

macd = float(latest["MACD"])
macd_signal = float(latest["MACD_Signal"])

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
# 5. TREND SCORE
# =========================================================

trend_score = 0

if close > ma7:
    trend_score += 1
else:
    trend_score -= 1

if close > ma30:
    trend_score += 1
else:
    trend_score -= 1

if ma7 > ma30:
    trend_score += 1
else:
    trend_score -= 1

if macd > macd_signal:
    trend_score += 1
else:
    trend_score -= 1

if momentum7 > 0:
    trend_score += 1
else:
    trend_score -= 1

if momentum30 > 0:
    trend_score += 1
else:
    trend_score -= 1


if trend_score >= 4:
    trend = "BULLISH"

elif trend_score <= -4:
    trend = "BEARISH"

else:
    trend = "NEUTRAL"


# =========================================================
# 6. MOMENTUM
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
# 7. RSI
# =========================================================

if rsi >= 70:

    rsi_status = "OVERBOUGHT"

elif rsi <= 30:

    rsi_status = "OVERSOLD"

else:

    rsi_status = "NORMAL"


# =========================================================
# 8. VOLATILITY
# =========================================================

volatility_percent = volatility * 100

if volatility_percent < 1:

    volatility_status = "LOW"

elif volatility_percent < 2:

    volatility_status = "MEDIUM"

else:

    volatility_status = "HIGH"


# =========================================================
# 9. RISK SCORE
# =========================================================

risk_score = 50

if volatility_percent >= 2:

    risk_score += 25

elif volatility_percent >= 1:

    risk_score += 10

else:

    risk_score -= 10


if rsi >= 70 or rsi <= 30:

    risk_score += 10


if abs(momentum7) > 0.05:

    risk_score += 10


if relative_volume > 2:

    risk_score += 5


risk_score = max(
    0,
    min(100, risk_score)
)


if risk_score >= 70:

    risk_level = "HIGH"

elif risk_score >= 40:

    risk_level = "MEDIUM"

else:

    risk_level = "LOW"


# =========================================================
# 10. SENTIMENT
# =========================================================

# Temporary sentiment value.
#
# Later this will come directly from
# sentiment.py / FinBERT.

sentiment_score = 0.0072

if sentiment_score > 0.15:

    sentiment = "POSITIVE"

elif sentiment_score < -0.15:

    sentiment = "NEGATIVE"

else:

    sentiment = "NEUTRAL"


# =========================================================
# 11. OVERALL AI SCORE
# =========================================================

# Convert trend to score

if trend == "BULLISH":

    trend_value = 75

elif trend == "BEARISH":

    trend_value = 25

else:

    trend_value = 50


# Convert sentiment to score

sentiment_value = (
    50 + sentiment_score * 50
)

# Combine signals

overall_score = (
    trend_value * 0.40
    +
    sentiment_value * 0.25
    +
    (100 - risk_score) * 0.35
)

overall_score = max(
    0,
    min(100, overall_score)
)


# =========================================================
# 12. FINAL OUTLOOK
# =========================================================

if overall_score >= 65:

    outlook = "POSITIVE"

elif overall_score <= 35:

    outlook = "NEGATIVE"

else:

    outlook = "NEUTRAL"


# =========================================================
# 13. GENERATE AI INSIGHT
# =========================================================

insight_parts = []

if trend == "BULLISH":

    insight_parts.append(
        "TCS is showing bullish technical signals."
    )

elif trend == "BEARISH":

    insight_parts.append(
        "TCS is showing bearish technical signals."
    )

else:

    insight_parts.append(
        "TCS is showing mixed technical signals."
    )


if sentiment == "POSITIVE":

    insight_parts.append(
        "Recent financial news sentiment is positive."
    )

elif sentiment == "NEGATIVE":

    insight_parts.append(
        "Recent financial news sentiment is negative."
    )

else:

    insight_parts.append(
        "Recent financial news sentiment is neutral."
    )


if risk_level == "HIGH":

    insight_parts.append(
        "Volatility indicates elevated market risk."
    )

elif risk_level == "MEDIUM":

    insight_parts.append(
        "Market conditions indicate moderate risk."
    )

else:

    insight_parts.append(
        "Market risk is relatively low."
    )


final_insight = " ".join(
    insight_parts
)


# =========================================================
# 14. DISPLAY FINAL RESULT
# =========================================================

print("\n")
print("=" * 55)
print("           TCS AI FINANCIAL ANALYSIS")
print("=" * 55)

print(
    f"\nCurrent Price      : ₹{close:.2f}"
)

print(
    f"Trend              : {trend}"
)

print(
    f"Trend Score        : {trend_score}"
)

print(
    f"Momentum           : {momentum_status}"
)

print(
    f"RSI                : {rsi:.2f}"
)

print(
    f"RSI Status         : {rsi_status}"
)

print(
    f"Volatility         : {volatility_percent:.2f}%"
)

print(
    f"Volatility Status  : {volatility_status}"
)

print(
    f"Risk Score         : {risk_score}/100"
)

print(
    f"Risk Level         : {risk_level}"
)

print(
    f"News Sentiment     : {sentiment}"
)

print(
    f"Sentiment Score    : {sentiment_score:.4f}"
)

print(
    f"Overall AI Score   : {overall_score:.2f}/100"
)

print(
    f"Overall Outlook    : {outlook}"
)

print("\nAI INSIGHT:")
print(final_insight)

print("=" * 55)