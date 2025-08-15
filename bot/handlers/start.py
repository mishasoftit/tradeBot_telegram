from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import filters
from bot.keyboards.main_menu import main_menu_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """Handle /start command and display main menu"""
    await state.clear()  # Clear any existing state
    await message.answer(
        "🚀 Welcome to Crypto Trading Bot!",
        reply_markup=main_menu_keyboard()
    )

@router.message(filters.Text(contains="🔙 Back"))
async def cmd_back(message: types.Message, state: FSMContext):
    """Handle back navigation"""
    await state.clear()
    await message.answer(
        "⬅️ Returning to main menu",
        reply_markup=main_menu_keyboard()
    )