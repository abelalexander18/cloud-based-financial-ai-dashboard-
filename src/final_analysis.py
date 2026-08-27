import json
import subprocess
import re


# =========================================================
# 1. RUN SENTIMENT PIPELINE
# =========================================================

print("\nRunning news + sentiment analysis...\n")

result = subprocess.run(
    ["python", "src/sentiment.py"],
    capture_output=True,
    text=True
)

output = result.stdout

print(output)


# =========================================================
# 2. EXTRACT OVERALL SENTIMENT
# =========================================================

score_match = re.search(
    r"OVERALL SENTIMENT SCORE:\s*([-+]?\d*\.?\d+)",
    output,
    re.IGNORECASE
)

sentiment_match = re.search(
    r"OVERALL SENTIMENT:\s*(POSITIVE|NEGATIVE|NEUTRAL)",
    output,
    re.IGNORECASE
)


if score_match:

    sentiment_score = float(
        score_match.group(1)
    )

else:

    sentiment_score = 0


if sentiment_match:

    sentiment = sentiment_match.group(1)

else:

    sentiment = "NEUTRAL"


# =========================================================
# 3. RUN TECHNICAL / RISK ANALYSIS
# =========================================================

risk_result = subprocess.run(
    ["python", "src/risk_model.py"],
    capture_output=True,
    text=True
)

risk_output = risk_result.stdout

print(risk_output)


# =========================================================
# 4. EXTRACT RISK VALUES
# =========================================================

price_match = re.search(
    r"Current Price\s*:\s*₹([\d.]+)",
    risk_output
)

trend_match = re.search(
    r"Trend\s*:\s*(BULLISH|BEARISH|NEUTRAL)",
    risk_output
)

momentum_match = re.search(
    r"Momentum\s*:\s*(.+)",
    risk_output
)

rsi_match = re.search(
    r"RSI\s*:\s*([\d.]+)",
    risk_output
)

volatility_match = re.search(
    r"Volatility\s*:\s*([\d.]+)%",
    risk_output
)

risk_score_match = re.search(
    r"Risk Score\s*:\s*(\d+)/100",
    risk_output
)

risk_level_match = re.search(
    r"Risk Level\s*:\s*(LOW|MEDIUM|HIGH)",
    risk_output
)


price = (
    float(price_match.group(1))
    if price_match else 0
)

trend = (
    trend_match.group(1)
    if trend_match else "NEUTRAL"
)

momentum = (
    momentum_match.group(1).strip()
    if momentum_match else "UNKNOWN"
)

rsi = (
    float(rsi_match.group(1))
    if rsi_match else 0
)

volatility = (
    float(volatility_match.group(1))
    if volatility_match else 0
)

risk_score = (
    int(risk_score_match.group(1))
    if risk_score_match else 50
)

risk_level = (
    risk_level_match.group(1)
    if risk_level_match else "MEDIUM"
)


# =========================================================
# 5. CALCULATE OVERALL AI SCORE
# =========================================================

if trend == "BULLISH":

    trend_value = 75

elif trend == "BEARISH":

    trend_value = 25

else:

    trend_value = 50


sentiment_value = (
    50 + sentiment_score * 50
)


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
# 6. DETERMINE OUTLOOK
# =========================================================

if overall_score >= 65:

    outlook = "POSITIVE"

elif overall_score <= 35:

    outlook = "NEGATIVE"

else:

    outlook = "NEUTRAL"


# =========================================================
# 7. GENERATE FINAL INSIGHT
# =========================================================

if trend == "BULLISH":

    trend_text = (
        "TCS is showing bullish technical momentum."
    )

elif trend == "BEARISH":

    trend_text = (
        "TCS is showing bearish technical momentum."
    )

else:

    trend_text = (
        "TCS is showing mixed technical signals."
    )


if sentiment == "POSITIVE":

    sentiment_text = (
        "Recent financial news sentiment is positive."
    )

elif sentiment == "NEGATIVE":

    sentiment_text = (
        "Recent financial news sentiment is negative."
    )

else:

    sentiment_text = (
        "Recent financial news sentiment is neutral."
    )


if risk_level == "HIGH":

    risk_text = (
        "Market volatility indicates elevated risk."
    )

elif risk_level == "MEDIUM":

    risk_text = (
        "Market conditions indicate moderate risk."
    )

else:

    risk_text = (
        "Market risk is relatively low."
    )


insight = (
    trend_text + " "
    + sentiment_text + " "
    + risk_text
)


# =========================================================
# 8. CREATE FINAL JSON
# =========================================================

analysis = {

    "company": "TCS",

    "ticker": "TCS.NS",

    "current_price": round(
        price,
        2
    ),

    "trend": trend,

    "momentum": momentum,

    "rsi": round(
        rsi,
        2
    ),

    "volatility": round(
        volatility,
        2
    ),

    "risk_score": risk_score,

    "risk_level": risk_level,

    "sentiment": sentiment,

    "sentiment_score": round(
        sentiment_score,
        4
    ),

    "overall_score": round(
        overall_score,
        2
    ),

    "outlook": outlook,

    "ai_insight": insight
}


# =========================================================
# 9. SAVE JSON
# =========================================================

with open(
    "data/final_analysis.json",
    "w"
) as file:

    json.dump(
        analysis,
        file,
        indent=4
    )


# =========================================================
# 10. DISPLAY
# =========================================================

print("\n")
print("=" * 60)
print("             FINAL AI ANALYSIS")
print("=" * 60)

print(
    json.dumps(
        analysis,
        indent=4
    )
)

print("=" * 60)

print(
    "\nSaved to: data/final_analysis.json"
)