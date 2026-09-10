from .supabase_client import supabase

# ==========================================
# COMPANY DATA
# ==========================================

def get_companies():
    """Retrieve all companies from Supabase."""

    response = (
        supabase
        .table("companies")
        .select("*")
        .execute()
    )

    return response.data


def get_company_by_ticker(ticker):
    """Retrieve a company using its stock ticker."""

    response = (
        supabase
        .table("companies")
        .select("*")
        .eq("ticker", ticker)
        .single()
        .execute()
    )

    return response.data


# ==========================================
# MARKET DATA
# ==========================================

def get_market_data(company_id, limit=100):
    """Retrieve market data for a company."""

    response = (
        supabase
        .table("stock_market_data")
        .select("*")
        .eq("company_id", company_id)
        .order("date", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data


def get_latest_market_data(company_id):
    """Retrieve the latest market-data record."""

    response = (
        supabase
        .table("stock_market_data")
        .select("*")
        .eq("company_id", company_id)
        .order("date", desc=True)
        .limit(1)
        .execute()
    )

    return response.data


# ==========================================
# PREDICTIONS
# ==========================================

def get_predictions(company_id, limit=100):
    """Retrieve prediction records for a company."""

    response = (
        supabase
        .table("predictions")
        .select("*")
        .eq("company_id", company_id)
        .order("prediction_date", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data


# ==========================================
# RISK ANALYSIS
# ==========================================

def get_risk_analysis(company_id, limit=10):
    """Retrieve risk-analysis records for a company."""

    response = (
        supabase
        .table("risk_analysis")
        .select("*")
        .eq("company_id", company_id)
        .order("analyzed_at", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data


def get_latest_risk_analysis(company_id):
    """Retrieve the latest risk analysis."""

    response = (
        supabase
        .table("risk_analysis")
        .select("*")
        .eq("company_id", company_id)
        .order("analyzed_at", desc=True)
        .limit(1)
        .execute()
    )

    return response.data


# ==========================================
# FINAL AI ANALYSIS
# ==========================================

def get_final_analysis(company_id, limit=10):
    """Retrieve final AI-analysis records."""

    response = (
        supabase
        .table("final_analysis")
        .select("*")
        .eq("company_id", company_id)
        .order("analyzed_at", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data


def get_latest_final_analysis(company_id):
    """Retrieve the latest final AI analysis."""

    response = (
        supabase
        .table("final_analysis")
        .select("*")
        .eq("company_id", company_id)
        .order("analyzed_at", desc=True)
        .limit(1)
        .execute()
    )

    return response.data
# ==========================================
# SENTIMENT / NEWS
# ==========================================

def get_sentiment_analysis(company_id, limit=20):
    """Retrieve news sentiment records for a company."""

    response = (
        supabase
        .table("sentiment_analysis")
        .select("*")
        .eq("company_id", company_id)
        .order("analyzed_at", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data


def get_latest_sentiment_analysis(company_id):
    """Retrieve the latest news sentiment record."""

    response = (
        supabase
        .table("sentiment_analysis")
        .select("*")
        .eq("company_id", company_id)
        .order("analyzed_at", desc=True)
        .limit(1)
        .execute()
    )

    return response.data