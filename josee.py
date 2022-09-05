import atexit
import json
import logging
import os
from time import time

from aiogram import Bot, Dispatcher, executor

import bot
from settings import *

start_time = time()

# Configure logging
logging.basicConfig(level = logging._nameToLevel[debug.upper()])

# Initialize bot and dispatcher
tg_bot = Bot(token = token)
dp = Dispatcher(tg_bot)

data = {}
files_dir = os.listdir("bot/data")
for i in files_dir:
  file = open(f"bot/data/{i}", "r")
  file_name = i[:i.find('.')]
  file_format = i[i.find('.')+1:]
  if file_format == "txt":
    data[file_name] = file.readlines()
  elif file_format == "json":
    data[file_name] = json.load(file)
  file.close
del files_dir


@atexit.register
def onExit():
  f = open('bot/data/notes.json', 'w')
  json.dump(data['notes'], f)
  f.close()

if __name__ == '__main__':
  # if check_version: check_updates()
  # if check_data: check_files()
  executor.start_polling(dp, on_startup = bot.startup, skip_updates = True)
  