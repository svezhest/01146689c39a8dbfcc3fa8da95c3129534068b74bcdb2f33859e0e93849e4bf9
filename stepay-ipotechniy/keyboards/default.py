from aiogram.types import ReplyKeyboardMarkup, KeyboardButton 
from aiogram.utils.keyboard import ReplyKeyboardBuilder

async def get_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=f"👤 Проанализировать каналы 👤"))
    builder.row(KeyboardButton(text=f"📋 Список компаний 📋"))
    builder.row(KeyboardButton(text=f"ℹ️ Помощь ℹ️"))
    
    menu_keyboard = builder.as_markup()
    menu_keyboard.resize_keyboard = True
    
    return menu_keyboard
