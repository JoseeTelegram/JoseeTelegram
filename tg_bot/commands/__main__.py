import logging

from aiogram import Dispatcher

import tg_bot


async def startup(dp: Dispatcher):
    logging.info("Configuring modules...")
    tg_bot.modules.setup(dp.bot, dp)
