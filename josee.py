from settings import *

import libs.colors as jColors
import libs.round as jRound
import libs.time as jTime

from PIL import Image as img

import sys
import logging
import platform
import time
import random
import psutil
import requests
import json
import asyncio
import atexit

import telebot
from telebot.async_telebot import AsyncTeleBot

settings = AsyncTeleBot(token)

log = telebot.logger
log.setLevel(debug)

ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
ch.setFormatter(formatter)

log.addHandler(ch)

startTime = time.time()

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

@settings.message_handler(["coin"])
async def cmd_coin(msg):
  if random.randint(0,1):
    answer = "Head"
  else:
    answer = "Tail"
  return await settings.reply_to(msg, f"You get a {answer}!")


@settings.message_handler(["sysfetch"])
async def cmd_sysfetch(msg):
  UpTime = jTime.getReadableTime(round(time.time() - startTime))
  return await settings.reply_to(msg,
  f"<b>Platform:</b> {platform.system()} {platform.release()}\n"
  f"<b>Architecture:</b> {platform.machine()}\n"
  f"<b>Uptime:</b> {UpTime[0]} days {UpTime[1]} hours {UpTime[2]} mins {UpTime[3]} secs\n"
  f"<b>CPU:</b> {round(psutil.cpu_freq()[0]*1000)}/{round(psutil.cpu_freq()[2])} GHz ({round(psutil.cpu_percent())}%)\n"
  f"<b>RAM:</b> {round(psutil.virtual_memory().used / (1024.0 * 2))}/{round(psutil.virtual_memory().total / (1024.0 * 2))} MB ({round(psutil.virtual_memory().percent)}%)\n"
  f"<b>IP:</b> {requests.get('http://icanhazip.com').text.rstrip()}\n",
  parse_mode = 'HTML')


@settings.message_handler(["random"])
async def cmd_random(msg):
  arg = msg.text.split()[1:]

  if not arg:
    return await settings.reply_to(msg, "Usage: /random <int>")

  try:
    return await settings.reply_to(msg, random.randrange(0, int(arg[0])))
  except ValueError:
    return await settings.reply_to(msg, f"{arg[0]} isn\'t a number.")


@settings.message_handler(["8ball"])
async def cmd_8ball(msg):
  return await settings.reply_to(msg, random.choice(data[0]['8ball']))


@settings.message_handler(["crypto"])
async def cmd_crypto(msg):
  await settings.reply_to(msg, 'Please wait...')
  res = "*Popular cryptocurrencies*\n"
  for i in data[0]['crypto']:
    # print("Requesting:", i)
    req = requests.get(f'https://data.messari.io/api/v1/assets/{i}/metrics').json()['data']['market_data']
    res += f"*{data[0]['crypto'][i]['name']} ({data[0]['crypto'][i]['short-name']})* - ${jRound.RoundTo(req['price_usd'])}"
    if req['percent_change_usd_last_1_hour']:   res += f" (1h: {jRound.RoundTo(req['percent_change_usd_last_1_hour'])}%"
    if req['percent_change_usd_last_24_hours']: res += f" 24h: {jRound.RoundTo(req['percent_change_usd_last_24_hours'])}%)"
    else: 
      if req['percent_change_usd_last_1_hour']: res += ")"
    res += "\n"
  return await settings.reply_to(msg, res, parse_mode = 'Markdown')


@settings.message_handler(["rgb"])
async def cmd_rgb(msg):
  arg = msg.text.split()[1:]

  if not arg:
    return await settings.reply_to(msg, "Usage: /rgb <r> <g> <b>")

  r = int(arg[0])
  g = int(arg[1])
  b = int(arg[2])

  try: 
    photo = img.new("RGB", (128, 128), (r, g, b))
  except: 
    return await settings.reply_to(msg, "Error, usage: /rgb <r> <g> <b>")

  await settings.send_photo(msg.chat.id, photo,
  f"*RGB:* {r}, {g}, {b}\n"
  f"*HEX:* #{''.join(str(i) for i in jColors.rgb2hex(r, g, b))}\n"
  f"*HSV:* {', '.join(str(round(i)) for i in jColors.rgb2hsv(r, g, b))}\n"
  f"*CMYK:* {', '.join(str(round(i)) for i in jColors.rgb2cmyk(r, g, b))}\n",
  parse_mode = "Markdown")

  return photo.close()


@settings.message_handler(["cat"])
async def cmd_cat(msg):
  return await settings.send_message(msg.chat.id, ' '.join(msg.text.split()[1:]))


@settings.message_handler(["remind"])
async def cmd_remind(msg):
  arg = msg.text.split()[1:]

  if not arg:
    return await settings.reply_to(msg, "Usage: /remind <time> <message>")
  
  if arg[0].isdigit():
    time = arg[0]
  else:
    if not arg[0][0].isdigit():
      return await settings.reply_to(msg, "Argument doesn't contain a number.")
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
          return await settings.reply_to(msg, f"Argument is not entered in format. Example: 10sec/30min/1hour or 10s/30m/1h.")
        break
      
  await settings.reply_to(msg, f"Ugh... fine, I'll remind you in {time} seconds.")
  await asyncio.sleep(time)
  
  if msg.from_user.id != msg.chat.id:
    # await bot.forward_message(msg.from_user.id, msg.chat.id, msg.id)
    return await settings.send_message(msg.chat.id, f"@{msg.from_user.username}, remind: {' '.join(arg[1:])}")
 
  return await settings.send_message(msg.chat.id, f"Remind: {' '.join(arg[1:])}")


@settings.message_handler(["note"])
async def cmd_note(msg):
  arg = msg.text.split()[1:]

  if not arg:
    return await settings.reply_to(msg, "Usage: /note <add/list/delete> <note>")
  
  if not notes.get(str(msg.chat.id)):
    notes[str(msg.chat.id)] = []

  if arg[0] == "add":
    if len(arg) == 1:
      return await settings.reply_to(msg, "Nothing to note here...")
    notes[str(msg.chat.id)].append(" ".join(arg[1:]))
    return await settings.reply_to(msg, "Note succesfully created.")

  elif arg[0] == "list":
    if not notes[str(msg.chat.id)]:
      return await settings.reply_to(msg, "You have no notes, to create new: /note add <note>")
    answer = "*Note List*\n"
    for i in range(0, len(notes[str(msg.chat.id)])):
      answer += f"{i+1}. {notes[str(msg.chat.id)][i]}\n"
    return await settings.reply_to(msg, answer, parse_mode = 'Markdown')
    
  elif arg[0] == "delete":
    if arg[1].isdigit():
      if int(arg[1]) == 0 or int(arg[1])-1 > len(notes[str(msg.chat.id)]):
        return await settings.reply_to(msg, "That note already doesn't exists.")
      del notes[str(msg.chat.id)][int(arg[1])-1]
      return await settings.reply_to(msg, "Note succesfully deleted.")
    elif arg[1] == "all":
      notes[str(msg.chat.id)].clear()
      return await settings.reply_to(msg, "All notes was deleted.")
    else:
      return await settings.reply_to(msg, "Usage: /note delete <number/\"all\">")

  else:
    return await settings.reply_to(msg, "Usage: /note <add/list/delete> <note>")


@settings.message_handler(["pussy"])
async def cmd_pussy(msg):
  try:
    img = requests.get('https://cataas.com/c').content
  except:
    print('\"cataas.com\" seems don\'t avalable, trying long API request...')
    try:
      img = requests.get(json.loads(requests.get('https://api.thecatapi.com/v1/images/search').content)[0]['url']).content
    except:
      return await settings.reply_to(msg, 'No one server is not avalable, sorry!')
  finally:
    return await settings.send_photo(msg.chat.id, img, "Here, take it, pervert!", parse_mode = "Markdown")


@settings.message_handler(["repeat"])
async def cmd_repeat(msg):
  arg = msg.text.split()[1:]  
  
  if not arg:
    return await settings.reply_to(msg, "Usage: /repeat <count> <message>")

  try:
    count = int(arg[0])
  except:
    return await settings.reply_to(msg, "Argument isn't number.")
  
  if count < 0:
    return await settings.reply_to(msg, "Argument isn't positive.")

  for _ in range(count):
    await settings.send_message(msg.chat.id, ' '.join(arg[1:]))
  
  return


@atexit.register
def onExit():
  f = open('notes.json', 'w')
  json.dump(notes, f)

asyncio.run(settings.polling(non_stop=True, interval=0))