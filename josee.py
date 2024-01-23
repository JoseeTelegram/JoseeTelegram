import logging

from aiogram import Bot, Dispatcher, executor

import tg_bot
from settings import *

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.getLevelName(debug.upper()))

    # Initialize modules
    modules = []

    # Starting modules
    for i in modules:
        i.start()

    # Initialize bot and dispatcher
    bot = Bot(token=token)
    dp = Dispatcher(bot)

    # Start polling bot
    executor.start_polling(dp, on_startup=tg_bot.startup, skip_updates=True)
