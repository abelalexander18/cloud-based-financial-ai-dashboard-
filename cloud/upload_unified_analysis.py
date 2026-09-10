import json
from datetime import datetime

from server_supabase_client import supabase_server


# ==========================================
# CONFIGURATION
# ==========================================

JSON_FILE = "data/unified_analysis.json"
TICKER = "TCS.NS"


# ==========================================
# LOAD UNIFIED ANALYSIS
# ==========================================

print("\nLoading unified AI analysis...")

with open(JSON_FILE, "r") as file:
    analysis = json.load(file)

print("Unified analysis loaded successfully.")


# ==========================================
# FIND COMPANY
# ==========================================

print("\nFinding company in Supabase...")

company_response = (
    supabase_server
    .table("companies")
    .select("id, name, ticker")
    .eq("ticker", TICKER)
    .execute()
)

if not company_response.data:
    raise Exception(f"Company with ticker {TICKER} not found.")

company = company_response.data[0]
company_id = company["id"]

print(f"Company found: {company['name']}")
print(f"Company ID: {company_id}")


# ==========================================
# 1. UPLOAD PRICE + DIRECTION PREDICTIONS
# ==========================================

print("\nProcessing predictions...")

market = analysis["market"]
price_prediction = analysis["price_prediction"]
direction_prediction = analysis["direction_prediction"]

prediction_date = price_prediction["prediction_date"]


# Price prediction
price_record = {
    "company_id": company_id,
    "prediction_date": prediction_date,
    "predicted_price": float(
        price_prediction["predicted_next_day_price"]
    ),
    "predicted_direction": None,
    "confidence": None,
    "model_name": price_prediction["model"]
}


# Direction prediction
direction_record = {
    "company_id": company_id,
    "prediction_date": direction_prediction["prediction_date"],
    "predicted_price": float(
        price_prediction["predicted_next_day_price"]
    ),
    "predicted_direction": direction_prediction["direction"],
    "confidence": round(
        float(direction_prediction["confidence"]) * 100,
        2
    ),
    "model_name": direction_prediction["model"]
}


prediction_records = [
    price_record,
    direction_record
]


# ==========================================
# UPLOAD PREDICTIONS
# ==========================================

for record in prediction_records:

    existing = (
        supabase_server
        .table("predictions")
        .select("id")
        .eq("company_id", record["company_id"])
        .eq("prediction_date", record["prediction_date"])
        .eq("model_name", record["model_name"])
        .execute()
    )

    if existing.data:

        print(
            f"Prediction already exists: "
            f"{record['model_name']}"
        )

    else:

        supabase_server \
            .table("predictions") \
            .insert(record) \
            .execute()

        print(
            f"Uploaded prediction: "
            f"{record['model_name']}"
        )


# ==========================================
# 2. UPLOAD SENTIMENT / NEWS
# ==========================================

print("\nProcessing news sentiment...")

articles = analysis.get("news", {}).get("articles", [])

sentiment_records = []

for article in articles:

    record = {
        "company_id": company_id,
        "headline": article.get("title"),
        "source": article.get("source"),
        "sentiment": article.get("sentiment"),
        "confidence": article.get("confidence"),
        "sentiment_score": article.get("sentiment_score"),
        "analyzed_at": article.get("published")
    }

    sentiment_records.append(record)


print(f"Found {len(sentiment_records)} news articles.")


# ==========================================
# UPLOAD SENTIMENT RECORDS
# ==========================================

for record in sentiment_records:

    existing = (
        supabase_server
        .table("sentiment_analysis")
        .select("id")
        .eq("company_id", company_id)
        .eq("headline", record["headline"])
        .execute()
    )

    if existing.data:

        print(
            f"Skipping duplicate article: "
            f"{record['headline'][:60]}"
        )

    else:

        supabase_server \
            .table("sentiment_analysis") \
            .insert(record) \
            .execute()

        print(
            f"Uploaded sentiment: "
            f"{record['sentiment']}"
        )


# ==========================================
# 3. UPLOAD RISK ANALYSIS
# ==========================================

print("\nProcessing risk analysis...")

risk = analysis["risk"]

risk_record = {
    "company_id": company_id,
    "risk_score": float(risk["score"]),
    "risk_level": risk["level"],
    "volatility": float(market["volatility"]),
    "rsi": float(market["rsi"]),
    "momentum": market["momentum"],
    "trend": market["trend"],
    "analyzed_at": datetime.now().isoformat()
}


existing_risk = (
    supabase_server
    .table("risk_analysis")
    .select("id")
    .eq("company_id", company_id)
    .eq("risk_score", risk_record["risk_score"])
    .eq("risk_level", risk_record["risk_level"])
    .execute()
)


if existing_risk.data:

    print("Identical risk analysis already exists.")

else:

    supabase_server \
        .table("risk_analysis") \
        .insert(risk_record) \
        .execute()

    print("Risk analysis uploaded.")


# ==========================================
# 4. UPLOAD FINAL ANALYSIS
# ==========================================

print("\nProcessing final AI analysis...")

sentiment = analysis["sentiment"]
overall = analysis["overall"]

final_record = {
    "company_id": company_id,
    "current_price": float(market["current_price"]),
    "trend": market["trend"],
    "momentum": market["momentum"],
    "rsi": float(market["rsi"]),
    "volatility": float(market["volatility"]),
    "risk_score": float(risk["score"]),
    "risk_level": risk["level"],
    "sentiment": sentiment["label"],
    "sentiment_score": float(sentiment["score"]),
    "overall_score": float(overall["score"]),
    "outlook": overall["outlook"],
    "ai_insight": overall["insight"],
    "analyzed_at": datetime.now().isoformat()
}


existing_final = (
    supabase_server
    .table("final_analysis")
    .select("id")
    .eq("company_id", company_id)
    .eq("current_price", final_record["current_price"])
    .eq("overall_score", final_record["overall_score"])
    .eq("outlook", final_record["outlook"])
    .execute()
)


if existing_final.data:

    print("Identical final analysis already exists.")

else:

    supabase_server \
        .table("final_analysis") \
        .insert(final_record) \
        .execute()

    print("Final AI analysis uploaded.")


# ==========================================
# COMPLETE
# ==========================================

print("\n==========================================")
print("UNIFIED AI ANALYSIS UPLOAD COMPLETE")
print("==========================================")