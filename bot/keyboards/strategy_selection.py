from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def strategy_selection_keyboard():
    """Keyboard for selecting trading strategy"""
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Starter ($100+)", callback_data="strategy_starter"),
        InlineKeyboardButton("Basic ($1,000+)", callback_data="strategy_basic"),
        InlineKeyboardButton("Intermediate ($5,000+)", callback_data="strategy_intermediate"),
        InlineKeyboardButton("Large ($10,000+)", callback_data="strategy_large"),
        InlineKeyboardButton("Institutional ($100,000+)", callback_data="strategy_institutional"),
        InlineKeyboardButton("🔙 Back", callback_data="back_to_main")
    )