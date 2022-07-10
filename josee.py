import atexit
import json
import logging
import os
from time import time as now

import requests
from aiogram import Bot, Dispatcher, executor

from modules.__main__ import startup
from settings import *

# Configure logging
logging.basicConfig(level=logging._nameToLevel[debug.upper()])

# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher(bot)

start_time = now()

print("Checking data files...")
files_data = ["8ball.txt", "crypto.json", "notes.json", "cat.jpg"]

if not os.path.exists("data"):
  os.mkdir("data")

files_dir = os.listdir("data")

for i in files_data:
  print(f"{i}... ", end="")
  if not os.path.exists(f"data/{i}"):
    print("fail, downloading the file")
    file = open(f"data/{i}", "w")
    file.write(requests.get(f"https://raw.githubusercontent.com/Josee-Yamamura/JoseeTelegram/main/data/{i}").text)
    file.close()
  else:
    print("ok")

print("\nReading data files...")

data = {}
for i in files_dir:
  file = open(f"data/{i}", "r")
  file_name = i[:i.find('.')]
  file_format = i[i.find('.')+1:]
  if file_format == "txt":
    data[file_name] = file.readlines()
  elif file_format == "json":
    data[file_name] = json.load(file)
  file.close

del files_data
del files_dir

if not os.path.exists("cache"):
  os.mkdir("cache")

print("\nBot starting...")

@atexit.register
def onExit():
  f = open('data/notes.json', 'w')
  json.dump(data['notes'], f)
  f.close()

if __name__ == '__main__':
  executor.start_polling(dp, on_startup=startup, skip_updates=True)
