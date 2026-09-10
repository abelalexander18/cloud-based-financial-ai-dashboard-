import json
from server_supabase_client import supabase_server


print("Loading risk analysis...")

with open("data/final_analysis.json", "r") as file:
    analysis = json.load(file)

print("Finding TCS company in Supabase...")

company_response = (
    supabase_server
    .table("companies")
    .select("id, name, ticker")
    .eq("ticker", analysis["ticker"])
    .single()
    .execute()
)

company = company_response.data

if not company:
    raise Exception("TCS company not found in Supabase")

company_id = company["id"]

print(f"Company found: {company['name']}")
print(f"Company ID: {company_id}")

risk_data = {
    "company_id": company_id,
    "risk_score": analysis["risk_score"],
    "risk_level": analysis["risk_level"],
    "volatility": analysis["volatility"],
    "rsi": analysis["rsi"],
    "momentum": analysis["momentum"],
    "trend": analysis["trend"]
}

print("\nChecking existing risk analysis...")

existing_response = (
    supabase_server
    .table("risk_analysis")
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
        float(latest["risk_score"]) == float(risk_data["risk_score"])
        and latest["risk_level"] == risk_data["risk_level"]
        and float(latest["volatility"]) == float(risk_data["volatility"])
        and float(latest["rsi"]) == float(risk_data["rsi"])
        and latest["momentum"] == risk_data["momentum"]
        and latest["trend"] == risk_data["trend"]
    )

    if same_analysis:
        print("Identical risk analysis already exists.")
        print("Skipping upload.")
    else:
        print("New risk analysis detected.")
        print("Uploading to Supabase...")

        response = (
            supabase_server
            .table("risk_analysis")
            .insert(risk_data)
            .execute()
        )

        print("\nRISK ANALYSIS UPLOAD SUCCESSFUL")
        print(response.data)

else:
    print("No existing risk analysis found.")
    print("Uploading to Supabase...")

    response = (
        supabase_server
        .table("risk_analysis")
        .insert(risk_data)
        .execute()
    )

    print("\nRISK ANALYSIS UPLOAD SUCCESSFUL")
    print(response.data)


print("\n==========================================")
print("RISK ANALYSIS PROCESS COMPLETE")
print("==========================================")