from db import Supabase

client = Supabase().createClient()

all_medicine_query_response = client.table("medicine").select("*").execute()

print(all_medicine_query_response)