from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import json
import os


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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# FIND JSON FILE
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "unified_analysis.json"
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

    if not os.path.exists(DATA_FILE):

        raise HTTPException(
            status_code=404,
            detail="Analysis data not found. Run unified_analysis.py first."
        )

    try:

        with open(
            DATA_FILE,
            "r"
        ) as file:

            analysis = json.load(file)

        return analysis

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )