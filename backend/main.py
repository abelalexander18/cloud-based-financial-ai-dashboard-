import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from cloud.data_repository import (
    get_company_by_ticker,
    get_market_data,
    get_latest_market_data,
    get_predictions,
    get_latest_risk_analysis,
    get_latest_final_analysis,
    get_sentiment_analysis
)


def calculate_market_metrics(market_history):
    """Calculate metrics from the historical rows returned by Supabase."""
    rows = [row for row in market_history if row.get("close_price") is not None]
    volumes = [float(row["volume"]) for row in market_history if row.get("volume") is not None]
    latest = market_history[0] if market_history else {}
    latest_volume = latest.get("volume")
    recent_volumes = volumes[:20]
    average_volume = sum(recent_volumes) / len(recent_volumes) if recent_volumes else None
    relative_volume = (
        float(latest_volume) / average_volume
        if latest_volume is not None and average_volume
        else None
    )

    peak = None
    maximum_drawdown = 0.0
    for row in reversed(rows):
        close_price = float(row["close_price"])
        peak = close_price if peak is None else max(peak, close_price)
        if peak:
            maximum_drawdown = max(maximum_drawdown, (peak - close_price) / peak * 100)

    return relative_volume, maximum_drawdown

load_dotenv()
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")


# =========================================================
# CREATE FASTAPI APP
# =========================================================

app = FastAPI(
    title="AI Financial Analytics API",
    description="Cloud API for the AI Financial Analytics Dashboard",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# ROOT ENDPOINT
# =========================================================

@app.get("/")
def root():

    return {
        "message": "AI Financial Analytics API is running",
        "status": "online"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# =========================================================
# GET TCS ANALYSIS
# =========================================================

@app.get("/api/analysis/TCS")
def get_tcs_analysis():

    try:

        company = get_company_by_ticker("TCS.NS")

        if not company:
            raise HTTPException(
                status_code=404,
                detail="TCS company not found in cloud database."
            )

        company_id = company["id"]

        market = get_latest_market_data(company_id)
        market_history = get_market_data(company_id, 1000)
        predictions = get_predictions(company_id, 10)
        risk = get_latest_risk_analysis(company_id)
        final_analysis = get_latest_final_analysis(company_id)
        sentiment = get_sentiment_analysis(company_id, 10)
        relative_volume, maximum_drawdown = calculate_market_metrics(market_history)

        return {
            "company": company,
            "market": market,
            "predictions": predictions,
            "risk": risk,
            "final_analysis": final_analysis,
            "sentiment": sentiment,
            "relative_volume": relative_volume,
            "maximum_drawdown": maximum_drawdown,
            "beta": 1.0,
            "beta_source": "Estimated/demo: no benchmark data available",
            "history": [
                {
                    "date": row.get("date"),
                    "close_price": row.get("close_price"),
                }
                for row in reversed(market_history)
                if row.get("date") is not None and row.get("close_price") is not None
            ]
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )