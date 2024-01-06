import logging
import time

from aiogram import Dispatcher
from settings import id

import tg_bot


async def startup(dp: Dispatcher):
    for i in id:
        logging.info(f"id: {i}")
        await dp.bot.send_message(i, f"<b>Start Polling at:</b> {time.time()}", "HTML")
    logging.info("Configuring modules...")
    tg_bot.modules.setup(dp)
