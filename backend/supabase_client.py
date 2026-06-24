import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise ValueError("Supabase credentials not found in environment variables")

# Create Supabase client with service role key for admin operations
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def get_supabase_client() -> Client:
    """Get Supabase client instance"""
    return supabase

