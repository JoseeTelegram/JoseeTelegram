import settings

from PIL import Image as img

import sys
import logging
import platform
import time
import random
import psutil
import requests
import json
import math
import asyncio
import atexit
import colors

import telebot
from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot(settings.token)
log = telebot.logger
log.setLevel(settings.debug_level)

ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
ch.setFormatter(formatter)

log.addHandler(ch)

startTime = round(time.time())

f = open('data.json', 'r')
data = json.load(f)
f.close()

try:
  f = open('notes.json', 'r')
  notes = json.load(f)
  f.close()
except:
  print("Something wrong with \"notes.json\"...",
  "If you run this bot first time, ignore this message\n",
  "But if not, try to check:",
  "1. Existing file in the root folder of the bot.",
  "2. Permission to read (and write) file.",
  "3. Correct file format as json.",
  sep = "\n")
  notes = {}

def RoundTo(num, digits=2):
  if num == 0: return 0
  scale = int(-math.floor(math.log10(abs(num - int(num))))) + digits - 1
  if scale < digits: scale = digits
  return round(num, scale)


# src: https://ru.stackoverflow.com/questions/499269
def getNearestValue(value: int, list: list):
    """ Returns the index of the nearest value in list. """
    list_of_difs = [abs(value - x) for x in list]
    return list_of_difs.index(min(list_of_difs))


def getRome(value: int):
  """ Converts integer in to Roman numerals system. """
  if value < 0: return False

  rome = {
      1:"I",
      5:"V",
      10:"X",
      50:"L",
      100:"C",
      500:"D",
      1000:"M"
  }
  
  near_int = list(rome.keys())[getNearestValue(value, list(rome.keys()))]
  res = rome[near_int]
  value -= near_int
  
  while value > 0:
      for key in rome.keys():
          if value >= key:
              value -= key
              res += rome[key]
  while value < 0:
      for key in rome.keys():
          if abs(value) <= key:
              value += key
              res = rome[key] + res
  return res


def getReadableTime(time: int):
  """ Converts time in seconds to human-readable version. """
  if time < 0: return False

  td = 0
  th = 0
  tm = 0
  ts = 0

  while True:
      if time >= 86400:
          td += 1
          time -= 86400
      elif time >= 3600:
          th += 1
          time -= 3600
      elif time >= 60:
          tm += 1
          time -= 60
      else:
          ts = time
          break
  
  return td, th, tm, ts


@bot.message_handler(["coin"])
async def cmd_coin(msg):
  if random.randint(0,1):
    answer = "Head"
  else:
    answer = "Tail"
  return await bot.reply_to(msg, f"You get a {answer}!")


@bot.message_handler(["sysfetch"])
async def cmd_sysfetch(msg):
  UpTime = getReadableTime(round(time.time()) - startTime)
  return await bot.reply_to(msg,
  f"<b>Platform:</b> {platform.system()} {platform.release()}\n"
  f"<b>Architecture:</b> {platform.machine()}\n"
  f"<b>Uptime:</b> {UpTime[0]} days {UpTime[1]} hours {UpTime[2]} mins {UpTime[3]} secs\n"
  f"<b>CPU:</b> {round(psutil.cpu_freq()[0]*1000)}/{round(psutil.cpu_freq()[2])} GHz ({round(psutil.cpu_percent())}%)\n"
  f"<b>RAM:</b> {round(psutil.virtual_memory().used / (1024.0 * 2))}/{round(psutil.virtual_memory().total / (1024.0 * 2))} MB ({round(psutil.virtual_memory().percent)}%)\n"
  f"<b>IP:</b> {requests.get('http://icanhazip.com').text.rstrip()}\n",
  parse_mode = 'HTML')


@bot.message_handler(["random"])
async def cmd_random(msg):
  arg = msg.text.split()[1:]
  if not arg:
    return await bot.reply_to(msg, "Usage: /random <int>")
  try:
    return await bot.reply_to(msg, random.randrange(0, int(arg[0])))
  except ValueError:
    return await bot.reply_to(msg, f"{arg[0]} isn\'t a number.")


@bot.message_handler(["8ball"])
async def cmd_8ball(msg):
  return await bot.reply_to(msg, random.choice(data[0]['8ball']))


@bot.message_handler(["crypto"])
async def cmd_crypto(msg):
  await bot.reply_to(msg, 'Please wait...')
  res = "*Popular cryptocurrencies*\n"
  for i in data[0]['crypto']:
    # print("Requesting:", i)
    req = requests.get(f'https://data.messari.io/api/v1/assets/{i}/metrics').json()['data']['market_data']
    res += f"*{data[0]['crypto'][i]['name']} ({data[0]['crypto'][i]['short-name']})* - ${RoundTo(req['price_usd'])}"
    if req['percent_change_usd_last_1_hour']:   res += f" (1h: {RoundTo(req['percent_change_usd_last_1_hour'])}%"
    if req['percent_change_usd_last_24_hours']: res += f" 24h: {RoundTo(req['percent_change_usd_last_24_hours'])}%)"
    else: 
      if req['percent_change_usd_last_1_hour']: res += ")"
    res += "\n"
  return await bot.reply_to(msg, res, parse_mode = 'Markdown')


@bot.message_handler(["rgb"])
async def cmd_rgb(msg):
  arg = msg.text.split()[1:]

  if not arg:
    return await bot.reply_to(msg, "Usage: /rgb <r> <g> <b>")

  r = int(arg[0])
  g = int(arg[1])
  b = int(arg[2])

  try: 
    photo = img.new("RGB", (128, 128), (r, g, b))
  except: 
    return await bot.reply_to(msg, "Error, usage: /rgb <r> <g> <b>")

  await bot.send_photo(msg.chat.id, photo,
  f"*RGB:* {r}, {g}, {b}\n"
  f"*HEX:* #{''.join(str(i) for i in colors.rgb2hex(r, g, b))}\n"
  f"*HSV:* {', '.join(str(round(i)) for i in colors.rgb2hsv(r, g, b))}\n"
  f"*CMYK:* {', '.join(str(round(i)) for i in colors.rgb2cmyk(r, g, b))}\n",
  parse_mode = "Markdown")

  return photo.close()


@bot.message_handler(["cat"])
async def cmd_cat(msg):
  return await bot.send_message(msg.chat.id, ' '.join(msg.text.split()[1:]))


@bot.message_handler(["remind"])
async def cmd_remind(msg):
  arg = msg.text.split()[1:]

  if not arg:
    return await bot.reply_to(msg, "Usage: /remind <time> <message>")
  
  if arg[0].isdigit():
    time = arg[0]
  else:
    if not arg[0][0].isdigit():
      return await bot.reply_to(msg, "Argument doesn't contain a number.")
    for sym in range(0, len(arg[0])):
      if not arg[0][sym].isdigit():
        time = int(arg[0][:sym])
        if arg[0][sym:] == "sec" or arg[0][sym:] == "s":
          pass
        elif arg[0][sym:] == "min" or arg[0][sym:] == "m":
          time *= 60
        elif arg[0][sym:] == "hour" or arg[0][sym:] == "h":
          time *= 3600
        else:
          return await bot.reply_to(msg, f"Argument is not entered in format. Example: 10sec/30min/1hour or 10s/30m/1h.")
        break
      
  await bot.reply_to(msg, f"Ugh... fine, I'll remind you in {time} seconds.")
  await asyncio.sleep(time)
  
  if msg.from_user.id != msg.chat.id:
    # await bot.forward_message(msg.from_user.id, msg.chat.id, msg.id)
    return await bot.send_message(msg.chat.id, f"@{msg.from_user.username}, remind: {' '.join(arg[1:])}")
 
  return await bot.send_message(msg.chat.id, f"Remind: {' '.join(arg[1:])}")


@bot.message_handler(["note"])
async def cmd_note(msg):
  arg = msg.text.split()[1:]

  if not notes.get(str(msg.chat.id)):
    notes[str(msg.chat.id)] = []

  if not arg:
    return await bot.reply_to(msg, "Usage: /note <add/list/delete> <note>")
  
  if arg[0] == "add":
    if len(arg) == 1:
      return await bot.reply_to(msg, "Nothing to note here...")
    notes[str(msg.chat.id)].append(" ".join(arg[1:]))
    return await bot.reply_to(msg, "Note succesfully created.")

  elif arg[0] == "list":
    if not notes[str(msg.chat.id)]:
      return await bot.reply_to(msg, "You have no notes, to create new: /note add <note>")
    answer = "*Note List*\n"
    for i in range(0, len(notes[str(msg.chat.id)])):
      answer += f"{i+1}. {notes[str(msg.chat.id)][i]}\n"
    return await bot.reply_to(msg, answer, parse_mode = 'Markdown')
    
  elif arg[0] == "delete":
    if arg[1].isdigit():
      if int(arg[1]) == 0 or int(arg[1])-1 > len(notes[str(msg.chat.id)]):
        return await bot.reply_to(msg, "That note already doesn't exists.")
      del notes[str(msg.chat.id)][int(arg[1])-1]
      return await bot.reply_to(msg, "Note succesfully deleted.")
    elif arg[1] == "all":
      notes[str(msg.chat.id)].clear()
      return await bot.reply_to(msg, "All notes was deleted.")
    else:
      return await bot.reply_to(msg, "Usage: /note delete <number/\"all\">")

  else:
    return await bot.reply_to(msg, "Usage: /note <add/list/delete> <note>")

@atexit.register
def onExit():
  f = open('notes.json', 'w')
  json.dump(notes, f)

asyncio.run(bot.polling(none_stop=True, interval=0))