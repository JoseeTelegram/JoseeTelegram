import atexit
import json
import logging
from time import time

from aiogram import Bot, Dispatcher, executor

from modules.__main__ import startup
from settings import *
from utils.check_files import check_files
from utils.check_updates import check_updates

# Configure logging
logging.basicConfig(level=logging._nameToLevel[debug.upper()])

# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher(bot)

start_time = time()

data = {}
files_dir = os.listdir("data")
for i in files_dir:
  file = open(f"data/{i}", "r")
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
  f = open('data/notes.json', 'w')
  json.dump(data['notes'], f)
  f.close()

if __name__ == '__main__':
  if check_version: check_updates()
  if check_data: check_files()
  print("\nBot starting...")
  executor.start_polling(dp, on_startup=startup, skip_updates=True)
  