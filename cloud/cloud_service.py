from supabase_client import supabase
from server_supabase_client import supabase_server


# ==========================================
# COMPANY CLOUD OPERATIONS
# ==========================================

def add_company(name, ticker):
    """
    Add a company to Supabase Cloud Database.
    """

    try:
        response = supabase_server.table("companies").insert({
            "name": name,
            "ticker": ticker
        }).execute()

        print("Company added successfully!")
        return response.data

    except Exception as e:
        print("Error adding company:", e)
        return None


def get_companies():
    """
    Retrieve all companies from Supabase.
    """

    try:
        response = supabase.table("companies").select("*").execute()

        return response.data

    except Exception as e:
        print("Error retrieving companies:", e)
        return None


# ==========================================
# MARKET DATA CLOUD OPERATIONS
# ==========================================

def get_market_data(company_id, limit=100):
    """
    Retrieve market data for a company.
    """

    try:
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

    except Exception as e:
        print("Error retrieving market data:", e)
        return None


def get_latest_market_data(company_id):
    """
    Retrieve the latest market data for a company.
    """

    try:
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

    except Exception as e:
        print("Error retrieving latest market data:", e)
        return None


# ==========================================
# PREDICTION CLOUD OPERATIONS
# ==========================================

def get_predictions(company_id, limit=100):
    """
    Retrieve prediction records for a company.
    """

    try:
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

    except Exception as e:
        print("Error retrieving predictions:", e)
        return None


# ==========================================
# RISK ANALYSIS CLOUD OPERATIONS
# ==========================================

def get_risk_analysis(company_id, limit=10):
    """
    Retrieve risk analysis records for a company.
    """

    try:
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

    except Exception as e:
        print("Error retrieving risk analysis:", e)
        return None


# ==========================================
# FINAL AI ANALYSIS CLOUD OPERATIONS
# ==========================================

def get_final_analysis(company_id, limit=10):
    """
    Retrieve final AI analysis records for a company.
    """

    try:
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

    except Exception as e:
        print("Error retrieving final analysis:", e)
        return None


def get_latest_final_analysis(company_id):
    """
    Retrieve the latest final AI analysis for a company.
    """

    try:
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

    except Exception as e:
        print("Error retrieving latest final analysis:", e)
        return None


# ==========================================
# TEST CLOUD OPERATIONS
# ==========================================

if __name__ == "__main__":

    print("\n==========================================")
    print("CLOUD DATA RETRIEVAL TEST")
    print("==========================================")

    # TCS company ID
    company_id = 2

    print("\n1. Companies:")
    companies = get_companies()
    print(companies)

    print("\n2. Latest market data:")
    market_data = get_latest_market_data(company_id)
    print(market_data)

    print("\n3. Latest predictions:")
    predictions = get_predictions(company_id, limit=5)
    print(predictions)

    print("\n4. Risk analysis:")
    risk = get_risk_analysis(company_id, limit=5)
    print(risk)

    print("\n5. Latest final AI analysis:")
    final_analysis = get_latest_final_analysis(company_id)
    print(final_analysis)

    print("\n==========================================")
    print("CLOUD RETRIEVAL TEST COMPLETE")
    print("==========================================")