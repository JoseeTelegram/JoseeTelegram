import asyncio
import atexit
import json
import logging
import os
import platform
import random
import sys
import time

import psutil
import requests
import telebot
from PIL import Image as img
from telebot.async_telebot import AsyncTeleBot

import libs.colors as jColors
import libs.round as jRound
import libs.time as jTime
from settings import *

bot = AsyncTeleBot(token)
log = telebot.logger
log.setLevel(debug)

ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
ch.setFormatter(formatter)

log.addHandler(ch)

start_time = time.time()

print("Checking data files...")

files_data = ["8ball.txt", "crypto.json", "notes.json"]

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

print("\nBot starting...")

# @bot.message_handler(content_types=["text"])
# async def mention(msg):
#   my = await bot.get_me()
#   print(my.username)
#   if msg.text == f"@{my.username}":
#     await bot.send_message(msg.chat.id, "https://github.com/Josee-Yamamura/JoseeTelegram")


@bot.message_handler(["coin"])
async def cmd_coin(msg):
  return await bot.reply_to(msg, f"You get a {['Head', 'Tail'][random.randint(0,1)]}!")


@bot.message_handler(["sysfetch"])
async def cmd_sysfetch(msg):
  up_time = jTime.getReadableTime(round(time.time() - start_time))
  return await bot.reply_to(msg,
  f"<b>Platform:</b> {platform.system()} {platform.release()}\n"
  f"<b>Architecture:</b> {platform.machine()}\n"
  f"<b>Uptime:</b> {up_time[0]} days {up_time[1]} hours {up_time[2]} mins {up_time[3]} secs\n"
  f"<b>CPU:</b> {round(psutil.cpu_freq()[0]*1000)}/{round(psutil.cpu_freq()[2])} GHz ({round(psutil.cpu_percent())}%)\n"
  f"<b>RAM:</b> {round(psutil.virtual_memory().used / (1024.0 * 2))}/{round(psutil.virtual_memory().total / (1024.0 * 2))} MB ({round(psutil.virtual_memory().percent)}%)\n"
  f"<b>IP:</b> {requests.get('http://icanhazip.com').text.rstrip()}\n",
  parse_mode = 'HTML')


@bot.message_handler(["random"])
async def cmd_random(msg):
  arg = msg.text.split()[1:]

  if not arg:
    return await bot.reply_to(msg, "Usage: /random <start> <end>")

  try:
    start = int(arg[0])
    if len(arg) == 1:
      return await bot.reply_to(msg, random.randrange(0, start))
    end = int(arg[1])
    if start < end:
      return await bot.reply_to(msg, random.randrange(start, end))
    elif start == end:
      return await bot.reply_to(msg, "Both integers are the same.")
    else:
      return await bot.reply_to(msg, random.randrange(end, start))
  except ValueError:
    return await bot.reply_to(msg, f"One of the arguments isn\'t an integer.")


@bot.message_handler(["8ball"])
async def cmd_8ball(msg):
  return await bot.reply_to(msg, random.choice(data['8ball']))


@bot.message_handler(["crypto"])
async def cmd_crypto(msg):
  answer = await bot.reply_to(msg, 'Please wait...')
  res = "*Popular cryptocurrencies*\n"
  for i in data['crypto']:
    # print("Requesting:", i)
    req = requests.get(f'https://data.messari.io/api/v1/assets/{i}/metrics').json()['data']['market_data']
    res += f"*{data['crypto'][i]['name']} ({data['crypto'][i]['short-name']})* - ${jRound.RoundTo(req['price_usd'])}"
    if req['percent_change_usd_last_1_hour']:   res += f" (1h: {jRound.RoundTo(req['percent_change_usd_last_1_hour'])}%"
    if req['percent_change_usd_last_24_hours']: res += f" 24h: {jRound.RoundTo(req['percent_change_usd_last_24_hours'])}%)"
    else: 
      if req['percent_change_usd_last_1_hour']: res += ")"
    res += "\n"
  return await bot.edit_message_text(res, msg.chat.id, answer.message_id, parse_mode = 'Markdown')


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
  f"*HEX:* #{''.join(str(i) for i in jColors.rgb2hex(r, g, b))}\n"
  f"*HSV:* {', '.join(str(round(i)) for i in jColors.rgb2hsv(r, g, b))}\n"
  f"*CMYK:* {', '.join(str(round(i)) for i in jColors.rgb2cmyk(r, g, b))}\n",
  parse_mode = "Markdown")

  return photo.close()


@bot.message_handler(["cat"])
async def cmd_cat(msg):
  res = msg.text[5:]
  if res: return await bot.send_message(msg.chat.id, res)


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

  if not arg:
    return await bot.reply_to(msg, "Usage: /note <add/list/delete> <note>")
  
  if not data['notes'].get(str(msg.chat.id)):
    data['notes'][str(msg.chat.id)] = []

  if arg[0] == "add":
    if len(arg) == 1:
      return await bot.reply_to(msg, "Nothing to note here...")
    data['notes'][str(msg.chat.id)].append(" ".join(arg[1:]))
    return await bot.reply_to(msg, "Note succesfully created.")

  elif arg[0] == "list":
    if not data['notes'][str(msg.chat.id)]:
      return await bot.reply_to(msg, "You have no data['notes'], to create new: /note add <note>")
    answer = "*Note List*\n"
    for i in range(0, len(data['notes'][str(msg.chat.id)])):
      answer += f"{i+1}. {data['notes'][str(msg.chat.id)][i]}\n"
    return await bot.reply_to(msg, answer, parse_mode = 'Markdown')
    
  elif arg[0] == "delete":
    if arg[1].isdigit():
      if int(arg[1]) == 0 or int(arg[1])-1 > len(data['notes'][str(msg.chat.id)]):
        return await bot.reply_to(msg, "That note already doesn't exists.")
      del data['notes'][str(msg.chat.id)][int(arg[1])-1]
      return await bot.reply_to(msg, "Note succesfully deleted.")
    elif arg[1] == "all":
      data['notes'][str(msg.chat.id)].clear()
      return await bot.reply_to(msg, "All notes was deleted.")
    else:
      return await bot.reply_to(msg, "Usage: /note delete <number/\"all\">")

  else:
    return await bot.reply_to(msg, "Usage: /note <add/list/delete> <note>")


@bot.message_handler(["pussy"])
async def cmd_pussy(msg):
  try:
    img = requests.get('https://cataas.com/c').content
  except:
    print('\"cataas.com\" seems don\'t avalable, trying long API request...')
    try:
      img = requests.get(json.loads(requests.get('https://api.thecatapi.com/v1/images/search').content)[0]['url']).content
    except:
      return await bot.reply_to(msg, 'No one server is not avalable, sorry!')
  finally:
    return await bot.send_photo(msg.chat.id, img, "Here, take it, pervert!", parse_mode = "Markdown")


@bot.message_handler(["repeat"])
async def cmd_repeat(msg):
  arg = msg.text.split()[1:]  
  
  if not arg:
    return await bot.reply_to(msg, "Usage: /repeat <count> <message>")

  try:
    count = int(arg[0])
  except:
    return await bot.reply_to(msg, "Argument isn't number.")
  
  if count < 0:
    return await bot.reply_to(msg, "Argument isn't positive.")

  for _ in range(count):
    await bot.send_message(msg.chat.id, ' '.join(arg[1:]))
  
  return


@atexit.register
def onExit():
  f = open('data/notes.json', 'w')
  json.dump(data['notes'], f)
  f.close()


print("Ready!")

asyncio.run(bot.polling(non_stop=True, interval=0))
