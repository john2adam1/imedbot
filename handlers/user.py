from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.inline import get_main_menu, get_cancel_keyboard, get_categories_keyboard
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
    await state.set_state(UserStates.waiting_for_category)
    await callback.message.edit_text(
        "Murojaat turini tanlang:",
        reply_markup=get_categories_keyboard()
    )

@user_router.callback_query(F.data.startswith("cat_"))
async def process_category(callback: types.CallbackQuery, state: FSMContext):
    category_map = {
        "cat_mobile": "📱 Mobil ilova va sayt bo'yicha",
        "cat_course": "🎓 Kurs sotib olish bo'yicha"
    }
    category = category_map.get(callback.data)
    await state.update_data(category=category)
    await state.set_state(UserStates.waiting_for_question)
    await callback.message.edit_text(
        f"Kategoriya: {category}\n\nSavolingizni yozib qoldiring:",
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
    data = await state.get_data()
    category = data.get("category", "Noma'lum")
    question = message.text
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    
    # Save to Supabase
    ticket = await create_ticket(user_id, message.message_id, question)
    
    if ticket:
        username_text = f" (@{message.from_user.username})" if message.from_user.username else ""
        # Forward to Admin Group
        admin_text = (
            "🆕 Yangi murojaat\n"
            f"#UID{user_id}\n"
            f"📂 Kategoriya: {category}\n"
            f"👤 Ism: {full_name}{username_text}\n"
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

@user_router.callback_query(F.data == "contact")
async def contact_info(callback: types.CallbackQuery):
    await callback.message.answer(
        "📞 Biz bilan aloqa:\n\n"
        "Telefon: +998 90 123 45 67\n"
        "Ish vaqti: 09:00 - 18:00"
    )
    await callback.answer()
