from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    """Create main menu keyboard"""
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False
    ).add(
        KeyboardButton("📈 Start Strategy"),
        KeyboardButton("📊 Statistics"),
    ).add(
        KeyboardButton("⚙️ Settings"),
        KeyboardButton("🛑 Stop Trading"),
    ).add(
        KeyboardButton("❓ Help")
    )