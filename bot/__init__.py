from aiogram import Dispatcher

from bot import modules


async def startup(dispatcher: Dispatcher):
    """Triggers on startup."""

    # Setup handlers
    modules.setup(dispatcher)
