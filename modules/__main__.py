import logging

from aiogram import Dispatcher

import modules


async def startup(dp: Dispatcher):
  logging.info("Configuring modules...")
  modules.setup(dp)
  logging.info("Start polling")
