from aiogram import Router, F, types, Bot
from database import get_ticket_by_admin_msg, answer_ticket
from config import ADMIN_GROUP_ID

admin_router = Router()

@admin_router.message(F.chat.id == ADMIN_GROUP_ID, F.reply_to_message)
async def admin_reply_handler(message: types.Message, bot: Bot):
    # Check if the replied message is from the bot (forwarded question)
    if not message.reply_to_message.from_user.is_bot:
        return

    admin_message_id = message.reply_to_message.message_id
    ticket = await get_ticket_by_admin_msg(admin_message_id)
    
    if not ticket:
        return

    user_id = ticket["user_id"]
    original_question = ticket["question_text"]
    reply_text = message.text
    
    reply_to_user = (
        f"❓ Sizning savolingiz: {original_question}\n"
        f"📩 Admindan javob: {reply_text}"
    )
    
    try:
        await bot.send_message(chat_id=user_id, text=reply_to_user)
        await answer_ticket(ticket["id"], reply_text)
        await message.reply("✅ Javob foydalanuvchiga yuborildi.")
    except Exception as e:
        await message.reply(f"❌ Xatolik: Foydalanuvchi botni bloklagan bo'lishi mumkin.\n{e}")
