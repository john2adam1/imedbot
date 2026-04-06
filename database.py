from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def create_ticket(user_id: int, user_message_id: int, question_text: str):
    data = {
        "user_id": user_id,
        "user_message_id": user_message_id,
        "question_text": question_text,
        "status": "pending"
    }
    response = supabase.table("tickets").insert(data).execute()
    return response.data[0] if response.data else None

async def update_ticket_admin_id(ticket_id: int, admin_message_id: int):
    supabase.table("tickets").update({"admin_message_id": admin_message_id}).eq("id", ticket_id).execute()

async def get_ticket_by_admin_msg(admin_message_id: int):
    response = supabase.table("tickets").select("*").eq("admin_message_id", admin_message_id).order("id", desc=True).limit(1).execute()
    return response.data[0] if response.data else None

async def answer_ticket(ticket_id: int, reply_text: str):
    supabase.table("tickets").update({"reply_text": reply_text, "status": "answered"}).eq("id", ticket_id).execute()
