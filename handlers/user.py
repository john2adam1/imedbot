from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.inline import get_main_menu, get_cancel_keyboard
from states.user_states import UserStates
from database import create_ticket, update_ticket_admin_id
from config import ADMIN_GROUP_ID

user_router = Router()

@user_router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Xush kelibsiz! Kerakli bo'limni tanlang:",
        reply_markup=get_main_menu()
    )

@user_router.callback_query(F.data == "ask_question")
async def ask_question(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.waiting_for_question)
    await callback.message.edit_text(
        "Savolingizni yozib qoldiring:",
        reply_markup=get_cancel_keyboard()
    )

@user_router.callback_query(F.data == "cancel")
async def cancel_action(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Kerakli bo'limni tanlang:",
        reply_markup=get_main_menu()
    )

@user_router.message(UserStates.waiting_for_question)
async def process_question(message: types.Message, state: FSMContext):
    question = message.text
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    
    # Save to Supabase
    ticket = await create_ticket(user_id, message.message_id, question)
    
    if ticket:
        # Forward to Admin Group
        admin_text = (
            "🆕 Yangi murojaat\n"
            f"#UID{user_id}\n"
            f"👤 Ism: {full_name}\n"
            f"💬 Savol: {question}\n"
            "Reply qilib javob bering ⬇️"
        )
        try:
            admin_msg = await message.bot.send_message(
                chat_id=ADMIN_GROUP_ID,
                text=admin_text
            )
            await update_ticket_admin_id(ticket["id"], admin_msg.message_id)
            await message.answer("Savolingiz adminga yuborildi. Tez orada javob olasiz!")
        except Exception as e:
            await message.answer("Xatolik yuz berdi. Iltimos keyinroq urinib ko'ring.")
            print(f"Error forwarding to admin: {e}")
    
    await state.clear()
    await message.answer("Asosiy menyu:", reply_markup=get_main_menu())

@user_router.callback_query(F.data == "my_info")
async def my_info(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    full_name = callback.from_user.full_name
    await callback.answer(f"ID: {user_id}\nIsm: {full_name}", show_alert=True)

@user_router.callback_query(F.data.in_(["admission_process", "location", "contact"]))
async def other_info(callback: types.CallbackQuery):
    # Placeholders for other buttons
    await callback.answer("Ushbu bo'lim tez orada ishga tushadi.", show_alert=True)
