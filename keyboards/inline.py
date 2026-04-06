from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✍️ Savol yozish", callback_data="ask_question")
    builder.button(text="📋 Qabul jarayoni", callback_data="admission_process")
    builder.button(text="📍 Bizning manzil", callback_data="location")
    builder.button(text="📞 Biz bilan aloqa", callback_data="contact")
    builder.button(text="👤 Mening ma'lumotlarim", callback_data="my_info")
    builder.adjust(1)
    return builder.as_markup()

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Bekor qilish", callback_data="cancel")
    return builder.as_markup()
