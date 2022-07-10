import logging
from josee import bot
from settings import id
from time import time, ctime

async def get_error(update, exception) -> None:
  logging.exception(exception)
  logging.debug(update)

  if id != 0:
    await bot.send_message(id, 
    "! ERROR FOUNDED !"
    f"\nTime: {ctime(time())}"
    f"\nCaused: {update['message']['from']['username']} ({update['message']['from']['first_name']} {update['message']['from']['last_name']})"
    f"\nFrom: @{update.message.chat.username} ({update.message.chat.type})"
    f"\nCommand: {update.message.text}"
    f"\nError: \"{exception}\"")
    
  return