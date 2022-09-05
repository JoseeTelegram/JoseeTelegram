from aiogram import Dispatcher

from tg_bot import modules


async def startup(dispatcher: Dispatcher):
    """Triggers on startup."""

    # Setup handlers
    modules.setup(dispatcher)
