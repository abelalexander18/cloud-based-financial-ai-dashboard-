import json
from server_supabase_client import supabase_server


# ==========================================
# LOAD FINAL AI ANALYSIS
# ==========================================

print("\nLoading final AI analysis...")

with open("data/final_analysis.json", "r") as file:
    analysis = json.load(file)

print("Analysis loaded successfully.")


# ==========================================
# FIND TCS COMPANY
# ==========================================

print("\nFinding TCS company in Supabase...")

company_response = (
    supabase_server
    .table("companies")
    .select("id, name, ticker")
    .eq("ticker", analysis["ticker"])
    .execute()
)

if not company_response.data:
    print("ERROR: TCS company not found in Supabase.")
    exit()

company = company_response.data[0]

company_id = company["id"]

print(f"Company found: {company['name']}")
print(f"Company ID: {company_id}")


# ==========================================
# PREPARE DATA
# ==========================================

record = {
    "company_id": company_id,
    "current_price": analysis["current_price"],
    "trend": analysis["trend"],
    "momentum": analysis["momentum"],
    "rsi": analysis["rsi"],
    "volatility": analysis["volatility"],
    "risk_score": analysis["risk_score"],
    "risk_level": analysis["risk_level"],
    "sentiment": analysis["sentiment"],
    "sentiment_score": analysis["sentiment_score"],
    "overall_score": analysis["overall_score"],
    "outlook": analysis["outlook"],
    "ai_insight": analysis["ai_insight"]
}


# ==========================================
# CHECK EXISTING FINAL ANALYSIS
# ==========================================

print("\nChecking existing final analysis...")

try:

    existing_response = (
        supabase_server
        .table("final_analysis")
        .select("*")
        .eq("company_id", company_id)
        .order("analyzed_at", desc=True)
        .limit(1)
        .execute()
    )

    existing = existing_response.data

    if existing:

        latest = existing[0]

        same_analysis = (
            float(latest["current_price"]) == float(record["current_price"])
            and latest["trend"] == record["trend"]
            and latest["momentum"] == record["momentum"]
            and float(latest["rsi"]) == float(record["rsi"])
            and float(latest["volatility"]) == float(record["volatility"])
            and float(latest["risk_score"]) == float(record["risk_score"])
            and latest["risk_level"] == record["risk_level"]
            and latest["sentiment"] == record["sentiment"]
            and float(latest["sentiment_score"]) == float(record["sentiment_score"])
            and float(latest["overall_score"]) == float(record["overall_score"])
            and latest["outlook"] == record["outlook"]
            and latest["ai_insight"] == record["ai_insight"]
        )

        if same_analysis:

            print("Identical final analysis already exists.")
            print("Skipping upload.")

        else:

            print("New final analysis detected.")
            print("Uploading to Supabase...")

            response = (
                supabase_server
                .table("final_analysis")
                .insert(record)
                .execute()
            )

            print("\nFINAL ANALYSIS UPLOAD SUCCESSFUL")
            print(response.data)

    else:

        print("No existing final analysis found.")
        print("Uploading to Supabase...")

        response = (
            supabase_server
            .table("final_analysis")
            .insert(record)
            .execute()
        )

        print("\nFINAL ANALYSIS UPLOAD SUCCESSFUL")
        print(response.data)

except Exception as e:

    print("\nERROR processing final analysis:")
    print(e)


print("\n==========================================")
print("FINAL ANALYSIS PROCESS COMPLETE")
print("==========================================")