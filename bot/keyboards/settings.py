from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def settings_keyboard():
    """Keyboard for bot settings"""
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("🔑 API Keys", callback_data="settings_api"),
        InlineKeyboardButton("📊 Risk Level", callback_data="settings_risk"),
        InlineKeyboardButton("🔔 Notifications", callback_data="settings_notify"),
        InlineKeyboardButton("🌓 Theme", callback_data="settings_theme"),
        InlineKeyboardButton("🔙 Back", callback_data="back_to_main")
    )

def api_key_management_keyboard():
    """Keyboard for API key management"""
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("➕ Add Exchange Key", callback_data="add_api_key"),
        InlineKeyboardButton("✏️ Edit Existing Key", callback_data="edit_api_key"),
        InlineKeyboardButton("🗑️ Delete Key", callback_data="delete_api_key"),
        InlineKeyboardButton("🔙 Back", callback_data="back_to_settings")
    )