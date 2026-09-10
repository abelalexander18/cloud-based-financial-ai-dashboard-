import json
import os
import pandas as pd
import numpy as np

from news import get_news
from transformers import pipeline


# =========================================================
# CONFIGURATION
# =========================================================

DATA_FILE = "data/processed_market_data.csv"
PRICE_PREDICTION_FILE = "data/random_forest_latest_prediction.json"
DIRECTION_PREDICTION_FILE = "data/direction_latest_prediction.json"
OUTPUT_FILE = "data/unified_analysis.json"

COMPANY = "TCS"
TICKER = "TCS.NS"


# =========================================================
# 1. LOAD PROCESSED MARKET DATA
# =========================================================

print("=" * 60)
print("TCS UNIFIED AI FINANCIAL ANALYSIS")
print("=" * 60)

print("\nLoading processed market data...")

df = pd.read_csv(DATA_FILE)

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

latest = df.iloc[-1]

print("Market data loaded.")
print("Latest date:", latest["Date"].date())


# =========================================================
# 2. GET CURRENT MARKET VALUES
# =========================================================

close = float(latest["Close"])

# Some values may already exist in processed data
# so use them directly when available.

ma_7 = float(latest["MA_7"])
ma_30 = float(latest["MA_30"])

rsi = float(latest["RSI"])
macd = float(latest["MACD"])
macd_signal = float(latest["MACD_Signal"])

volatility = float(
    df["Daily_Return"].rolling(20).std().iloc[-1]
)


# =========================================================
# 3. DETERMINE TREND
# =========================================================

trend_score = 0

if close > ma_7:
    trend_score += 1
else:
    trend_score -= 1

if close > ma_30:
    trend_score += 1
else:
    trend_score -= 1

if ma_7 > ma_30:
    trend_score += 1
else:
    trend_score -= 1

if macd > macd_signal:
    trend_score += 1
else:
    trend_score -= 1


if "Momentum_7" in df.columns:
    momentum_7 = float(latest["Momentum_7"])
else:
    momentum_7 = float(df["Close"].pct_change(7).iloc[-1])

if "Momentum_30" in df.columns:
    momentum_30 = float(latest["Momentum_30"])
else:
    momentum_30 = float(df["Close"].pct_change(30).iloc[-1])


if momentum_7 > 0:
    trend_score += 1
else:
    trend_score -= 1

if momentum_30 > 0:
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
# 4. MOMENTUM
# =========================================================

if momentum_7 > 0.03 and momentum_30 > 0.05:
    momentum_status = "STRONG POSITIVE"
elif momentum_7 > 0 or momentum_30 > 0:
    momentum_status = "MODERATE POSITIVE"
elif momentum_7 < -0.03 and momentum_30 < -0.05:
    momentum_status = "STRONG NEGATIVE"
else:
    momentum_status = "WEAK"


# =========================================================
# 5. RSI
# =========================================================

if rsi >= 70:
    rsi_status = "OVERBOUGHT"
elif rsi <= 30:
    rsi_status = "OVERSOLD"
else:
    rsi_status = "NORMAL"


# =========================================================
# 6. VOLATILITY
# =========================================================

volatility_percent = volatility * 100

if volatility_percent < 1:
    volatility_status = "LOW"
elif volatility_percent < 2:
    volatility_status = "MEDIUM"
else:
    volatility_status = "HIGH"


# =========================================================
# 7. RELATIVE VOLUME
# =========================================================

if "Relative_Volume" in df.columns:
    relative_volume = float(latest["Relative_Volume"])
else:
    volume_ma_20 = df["Volume"].rolling(20).mean().iloc[-1]
    relative_volume = float(latest["Volume"] / volume_ma_20)


# =========================================================
# 8. RISK SCORE
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

if abs(momentum_7) > 0.05:
    risk_score += 10

if relative_volume > 2:
    risk_score += 5

risk_score = max(0, min(100, risk_score))


if risk_score >= 70:
    risk_level = "HIGH"
elif risk_score >= 40:
    risk_level = "MEDIUM"
else:
    risk_level = "LOW"


# =========================================================
# 9. LOAD RANDOM FOREST PRICE PREDICTION
# =========================================================

print("\nLoading Random Forest price prediction...")

with open(PRICE_PREDICTION_FILE, "r") as file:
    price_prediction = json.load(file)

print("Price prediction loaded.")


# =========================================================
# 10. LOAD DIRECTION MODEL PREDICTION
# =========================================================

print("Loading direction prediction...")

with open(DIRECTION_PREDICTION_FILE, "r") as file:
    direction_prediction = json.load(file)

print("Direction prediction loaded.")


# =========================================================
# 11. GET NEWS
# =========================================================

print("\nFetching financial news...")

articles = get_news(COMPANY, max_articles=10)

print("Articles found:", len(articles))


# =========================================================
# 12. SENTIMENT ANALYSIS
# =========================================================

print("\nLoading FinBERT...")

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)

sentiment_scores = []

for article in articles:

    headline = article["title"]

    result = sentiment_pipeline(headline)[0]

    label = result["label"]
    confidence = result["score"]

    if label == "positive":
        score = confidence
    elif label == "negative":
        score = -confidence
    else:
        score = 0

    sentiment_scores.append(score)


if sentiment_scores:

    sentiment_score = (
        sum(sentiment_scores) /
        len(sentiment_scores)
    )

    if sentiment_score > 0.2:
        sentiment_label = "POSITIVE"
    elif sentiment_score < -0.2:
        sentiment_label = "NEGATIVE"
    else:
        sentiment_label = "NEUTRAL"

else:

    sentiment_score = 0.0
    sentiment_label = "NO DATA"


# =========================================================
# 13. OVERALL AI SCORE
# =========================================================

if trend == "BULLISH":
    trend_value = 75
elif trend == "BEARISH":
    trend_value = 25
else:
    trend_value = 50


sentiment_value = 50 + sentiment_score * 50

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
# 14. FINAL OUTLOOK
# =========================================================

if overall_score >= 65:
    outlook = "POSITIVE"
elif overall_score <= 35:
    outlook = "NEGATIVE"
else:
    outlook = "NEUTRAL"


# =========================================================
# 15. AI INSIGHT
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


if sentiment_label == "POSITIVE":
    insight_parts.append(
        "Recent financial news sentiment is positive."
    )
elif sentiment_label == "NEGATIVE":
    insight_parts.append(
        "Recent financial news sentiment is negative."
    )
elif sentiment_label == "NEUTRAL":
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


final_insight = " ".join(insight_parts)


# =========================================================
# 16. BUILD UNIFIED RESULT
# =========================================================

unified_analysis = {

    "company": COMPANY,
    "ticker": TICKER,

    "market": {
        "date": str(latest["Date"].date()),
        "current_price": round(close, 2),
        "ma_7": round(ma_7, 2),
        "ma_30": round(ma_30, 2),
        "rsi": round(rsi, 2),
        "rsi_status": rsi_status,
        "macd": round(macd, 2),
        "macd_signal": round(macd_signal, 2),
        "volatility": round(volatility_percent, 2),
        "volatility_status": volatility_status,
        "trend": trend,
        "trend_score": trend_score,
        "momentum": momentum_status,
        "relative_volume": round(relative_volume, 2)
    },

    "price_prediction": {
        "model": price_prediction["model"],
        "prediction_date": price_prediction["prediction_date"],
        "predicted_next_day_price":
            price_prediction["predicted_next_day_price"],
        "predicted_return":
            price_prediction["predicted_return"],
        "validation_mape":
            price_prediction["validation_mape"]
    },

    "direction_prediction": {
        "model": direction_prediction["model"],
        "prediction_date": direction_prediction["prediction_date"],
        "direction": direction_prediction["direction"],
        "confidence": direction_prediction["confidence"],
        "down_probability":
            direction_prediction["down_probability"],
        "up_probability":
            direction_prediction["up_probability"],
        "validation_accuracy":
            direction_prediction["validation_accuracy"]
    },

    "news": {
        "articles": articles
    },

    "sentiment": {
        "label": sentiment_label,
        "score": round(sentiment_score, 4)
    },

    "risk": {
        "score": risk_score,
        "level": risk_level
    },

    "overall": {
        "score": round(overall_score, 2),
        "outlook": outlook,
        "insight": final_insight
    }
}


# =========================================================
# 17. SAVE UNIFIED JSON
# =========================================================

with open(OUTPUT_FILE, "w") as file:
    json.dump(
        unified_analysis,
        file,
        indent=4
    )


# =========================================================
# 18. DISPLAY SUMMARY
# =========================================================

print("\n" + "=" * 60)
print("UNIFIED ANALYSIS COMPLETE")
print("=" * 60)

print(f"Current Price       : ₹{close:.2f}")

print(
    "Predicted Price     : "
    f"₹{price_prediction['predicted_next_day_price']:.2f}"
)

print(
    "Predicted Direction : "
    f"{direction_prediction['direction']}"
)

print(
    "Direction Confidence: "
    f"{direction_prediction['confidence'] * 100:.2f}%"
)

print(
    f"Sentiment           : {sentiment_label}"
)

print(
    f"Risk                : {risk_level} "
    f"({risk_score}/100)"
)

print(
    f"Overall AI Score    : "
    f"{overall_score:.2f}/100"
)

print(
    f"Outlook             : {outlook}"
)

print("\nSaved unified result to:")
print(OUTPUT_FILE)

print("=" * 60)