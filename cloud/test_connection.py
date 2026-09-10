from supabase_client import supabase

try:
    response = supabase.table("companies").select("*").execute()

    print("================================")
    print("SUPABASE CONNECTION SUCCESSFUL")
    print("================================")

    print(response.data)

except Exception as e:
    print("SUPABASE CONNECTION FAILED")
    print(e)