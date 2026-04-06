import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID", 0))

if not all([BOT_TOKEN, SUPABASE_URL, SUPABASE_KEY, ADMIN_GROUP_ID]):
    print("Warning: Some environment variables are missing.")
