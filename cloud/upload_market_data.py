import pandas as pd
from server_supabase_client import supabase_server


# ==========================================
# GET COMPANY ID
# ==========================================

company_response = (
    supabase_server
    .table("companies")
    .select("id")
    .eq("ticker", "TCS.NS")
    .execute()
)

if not company_response.data:
    print("TCS company not found in database.")
    exit()

company_id = company_response.data[0]["id"]

print(f"TCS Company ID: {company_id}")


# ==========================================
# LOAD MARKET DATA
# ==========================================

df = pd.read_csv("data/processed_market_data.csv")

print(f"Total records found: {len(df)}")


# ==========================================
# PREPARE DATA
# ==========================================

records = []

for _, row in df.iterrows():

    record = {
        "company_id": company_id,
        "date": row["Date"],
        "close_price": float(row["Close"]),
        "volume": int(row["Volume"]),
        "daily_return": float(row["Daily_Return"]),
        "ma_7": float(row["MA_7"]),
        "ma_30": float(row["MA_30"]),
        "ema_12": float(row["EMA_12"]),
        "ema_26": float(row["EMA_26"]),
        "macd": float(row["MACD"]),
        "macd_signal": float(row["MACD_Signal"]),
        "rsi": float(row["RSI"]),
        "volatility": float(row["Volatility"])
    }

    records.append(record)

# ==========================================
# DUPLICATE-SAFE CLOUD UPLOAD
# ==========================================

print("\nUploading market data to Supabase...")

batch_size = 500

for i in range(0, len(records), batch_size):

    batch = records[i:i + batch_size]

    supabase_server.table(
        "stock_market_data"
    ).upsert(
        batch,
        on_conflict="company_id,date",
        ignore_duplicates=True
    ).execute()

    print(
        f"Processed {min(i + batch_size, len(records))} "
        f"of {len(records)} records"
    )


print("\n===================================")
print("MARKET DATA UPLOAD COMPLETE")
print("===================================")