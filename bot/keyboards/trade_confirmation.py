from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def trade_confirmation_keyboard():
    """Keyboard for confirming trade execution"""
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("✅ Confirm", callback_data="confirm_trade"),
        InlineKeyboardButton("❌ Cancel", callback_data="cancel_trade")
    )