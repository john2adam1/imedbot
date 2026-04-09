from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✍️ Savol yozish", callback_data="ask_question")
    builder.button(text="📞 Biz bilan aloqa", callback_data="contact")
    builder.adjust(1)
    return builder.as_markup()

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Bekor qilish", callback_data="cancel")
    return builder.as_markup()

def get_categories_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📱 Mobil ilova va sayt bo'yicha", callback_data="cat_mobile")
    builder.button(text="🎓 Kurs sotib olish bo'yicha", callback_data="cat_course")
    builder.button(text="❌ Bekor qilish", callback_data="cancel")
    builder.adjust(1)
    return builder.as_markup()
