from aiogram import Dispatcher

from tg_bot import commands


async def startup(dispatcher: Dispatcher):
  """Triggers on startup."""
 
  # Setup handlers
  commands.setup(dispatcher)