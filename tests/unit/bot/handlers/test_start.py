import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram import types
from aiogram.fsm.context import FSMContext
from bot.handlers.start import cmd_start, cmd_back, router

@pytest.mark.asyncio
async def test_cmd_start():
    """Test /start command handler"""
    # Create mock message and state
    message = AsyncMock(spec=types.Message)
    message.answer = AsyncMock()
    state = AsyncMock(spec=FSMContext)
    state.clear = AsyncMock()
    
    # Call the command handler
    await cmd_start(message, state)
    
    # Verify state clearance
    state.clear.assert_awaited_once()
    
    # Verify response
    message.answer.assert_awaited_once_with(
        "🚀 Welcome to Crypto Trading Bot!",
        reply_markup=ANY
    )
    
    # Verify keyboard structure
    keyboard = message.answer.call_args[1]['reply_markup']
    assert isinstance(keyboard, types.ReplyKeyboardMarkup)
    assert len(keyboard.keyboard) == 2  # Two rows of buttons

@pytest.mark.asyncio
async def test_cmd_back():
    """Test back command handler"""
    # Create mock message and state
    message = AsyncMock(spec=types.Message)
    message.answer = AsyncMock()
    state = AsyncMock(spec=FSMContext)
    state.clear = AsyncMock()
    
    # Call the command handler
    await cmd_back(message, state)
    
    # Verify state clearance
    state.clear.assert_awaited_once()
    
    # Verify response
    message.answer.assert_awaited_once_with(
        "⬅️ Returning to main menu",
        reply_markup=ANY
    )

def test_router_initialization():
    """Test router handler registration"""
    # Verify router has the expected handlers
    assert len(router.message_handlers) == 2
    
    # Verify start command handler
    start_handler = router.message_handlers[0]
    assert start_handler.filters[0].commands == {"start"}
    
    # Verify back button handler
    back_handler = router.message_handlers[1]
    assert back_handler.filters[0].text == "🔙 Back"

# Helper for matching any object
class ANY:
    def __eq__(self, other):
        return True