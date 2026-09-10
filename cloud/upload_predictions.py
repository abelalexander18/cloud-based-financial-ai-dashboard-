import pandas as pd
from server_supabase_client import supabase_server


# ==========================================
# CONFIGURATION
# ==========================================

CSV_FILE = "data/random_forest_forecast.csv"
MODEL_NAME = "Random Forest"


# ==========================================
# LOAD DATA
# ==========================================

print("\nLoading prediction data...")

df = pd.read_csv(CSV_FILE)

print(f"Loaded {len(df)} prediction records.")


# ==========================================
# FIND TCS COMPANY
# ==========================================

print("\nFinding TCS company in Supabase...")

company_response = (
    supabase_server
    .table("companies")
    .select("id, name, ticker")
    .eq("ticker", "TCS.NS")
    .execute()
)

if not company_response.data:
    raise Exception("TCS company not found in Supabase.")

company = company_response.data[0]

company_id = company["id"]

print(f"Company found: {company['name']}")
print(f"Company ID: {company_id}")


# ==========================================
# PREPARE RECORDS
# ==========================================

records = []

for i in range(len(df)):

    row = df.iloc[i]

    prediction_date = str(row["Date"])

    actual_price = float(row["Actual_Price"])
    predicted_price = float(row["Predicted_Price"])

    # Direction relative to previous actual price
    if i > 0:
        previous_actual = float(df.iloc[i - 1]["Actual_Price"])

        if predicted_price > previous_actual:
            direction = "UP"
        elif predicted_price < previous_actual:
            direction = "DOWN"
        else:
            direction = "NEUTRAL"
    else:
        direction = "NEUTRAL"

    # Accuracy-based confidence proxy
    error_percentage = (
        abs(predicted_price - actual_price)
        / actual_price
    ) * 100

    confidence = max(
        0,
        min(100, 100 - error_percentage)
    )

    record = {
        "company_id": company_id,
        "prediction_date": prediction_date,
        "predicted_price": predicted_price,
        "predicted_direction": direction,
        "confidence": round(confidence, 2),
        "model_name": MODEL_NAME
    }

    records.append(record)


# ==========================================
# CHECK EXISTING PREDICTIONS
# ==========================================

print("\nChecking existing predictions in Supabase...")

existing_response = (
    supabase_server
    .table("predictions")
    .select("company_id, prediction_date, model_name")
    .eq("company_id", company_id)
    .execute()
)

existing_records = existing_response.data or []

existing_keys = {
    (
        record["company_id"],
        record["prediction_date"],
        record["model_name"]
    )
    for record in existing_records
}

print(f"Found {len(existing_records)} existing prediction records.")


# ==========================================
# FILTER NEW RECORDS
# ==========================================

new_records = []

for record in records:

    key = (
        record["company_id"],
        record["prediction_date"],
        record["model_name"]
    )

    if key not in existing_keys:
        new_records.append(record)


print(f"New records to upload: {len(new_records)}")
print(f"Duplicate records skipped: {len(records) - len(new_records)}")


# ==========================================
# UPLOAD NEW RECORDS
# ==========================================

if new_records:

    print("\nUploading new predictions to Supabase...")

    batch_size = 500

    for i in range(0, len(new_records), batch_size):

        batch = new_records[i:i + batch_size]

        response = (
            supabase_server
            .table("predictions")
            .insert(batch)
            .execute()
        )

        uploaded = min(
            i + batch_size,
            len(new_records)
        )

        print(
            f"Uploaded {uploaded} of "
            f"{len(new_records)} new prediction records"
        )

else:

    print("\nNo new prediction records to upload.")

# ==========================================
# COMPLETE
# ==========================================

print("\n==========================================")
print("PREDICTIONS UPLOAD SUCCESSFUL")
print("==========================================")