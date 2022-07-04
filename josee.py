import asyncio
import io
import json
import logging
import os
import platform
import random
import time

import psutil
import requests
from aiogram import Bot, Dispatcher, executor, types
from PIL import Image as IMG

import libs.colors as jColors
import libs.round as jRound
import libs.time as jTime
from settings import *

# Configure logging
logging.basicConfig(level=logging._nameToLevel[debug.upper()])

# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher(bot)

start_time = time.time()

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


@dp.message_handler(commands="coin")
async def cmd_coin(msg: types.Message):
  return await msg.reply(f"You get a {['Head', 'Tail'][random.randint(0,1)]}!")


@dp.message_handler(commands="sysfetch")
async def cmd_sysfetch(msg: types.Message):
  up_time = jTime.getReadableTime(round(time.time() - start_time))
  return await msg.reply(
  f"<b>Platform:</b> {platform.system()} {platform.release()}\n"
  f"<b>Architecture:</b> {platform.machine()}\n"
  f"<b>Uptime:</b> {up_time[0]} days {up_time[1]} hours {up_time[2]} mins {up_time[3]} secs\n"
  f"<b>CPU:</b> {round(psutil.cpu_freq()[0]*1000)}/{round(psutil.cpu_freq()[2])} GHz ({round(psutil.cpu_percent())}%)\n"
  f"<b>RAM:</b> {round(psutil.virtual_memory().used / (1024.0 * 2))}/{round(psutil.virtual_memory().total / (1024.0 * 2))} MB ({round(psutil.virtual_memory().percent)}%)\n"
  f"<b>IP:</b> {requests.get('http://icanhazip.com').text.rstrip()}\n", 'HTML')


@dp.message_handler(commands="random")
async def cmd_random(msg: types.Message):
  arg = msg.text.split()[1:]

  if not arg:
    return await msg.reply("Usage: /random <start> <end>")

  try:
    start = int(arg[0])
    if len(arg) == 1:
      return await msg.reply(random.randrange(0, start))
    end = int(arg[1])
    if start < end:
      return await msg.reply(random.randrange(start, end))
    elif start == end:
      return await msg.reply("Both integers are the same.")
    else:
      return await msg.reply(random.randrange(end, start))
  except ValueError:
    return await msg.reply(f"One of the arguments isn\'t an integer.")


@dp.message_handler(commands="8ball")
async def cmd_8ball(msg: types.Message):
  return await msg.reply(random.choice(data['8ball']))


@dp.message_handler(commands="crypto")
async def cmd_crypto(msg: types.Message):
  answer = await msg.reply('Please wait...')
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


@dp.message_handler(commands="rgb")
async def cmd_rgb(msg: types.Message):
  arg = msg.text.split()[1:]

  if not arg:
    return await msg.reply("Usage: /rgb <r> <g> <b>")

  r = int(arg[0])
  g = int(arg[1])
  b = int(arg[2])

  try:
    file_name = int(time.time())
    IMG.new("RGB", (128, 128), (r, g, b)).save(f"cache/{file_name}.png", bitmap_format="png")
    file = open(f"cache/{file_name}.png", "rb")
  except Exception as e:
    print(e)
    return await msg.reply("Error, usage: /rgb <r> <g> <b>")

  await bot.send_photo(msg.chat.id, file,
  f"*RGB:* {r}, {g}, {b}\n"
  f"*HEX:* #{''.join(str(i) for i in jColors.rgb2hex(r, g, b))}\n"
  f"*HSV:* {', '.join(str(round(i)) for i in jColors.rgb2hsv(r, g, b))}\n"
  f"*CMYK:* {', '.join(str(round(i)) for i in jColors.rgb2cmyk(r, g, b))}\n",
  parse_mode = "Markdown")

  os.remove(f"cache/{file_name}.png")
  return file.close()


@dp.message_handler(commands="cat")
async def cmd_cat(msg: types.Message):
  res = msg.text[5:]
  if res: return await bot.send_message(msg.chat.id, res)


@dp.message_handler(commands="remind")
async def cmd_remind(msg: types.Message):
  arg = msg.text.split()[1:]

  if not arg:
    return await msg.reply("Usage: /remind <time> <message>")
  
  if arg[0].isdigit():
    time = arg[0]
  else:
    if not arg[0][0].isdigit():
      return await msg.reply("Argument doesn't contain a number.")
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
          return await msg.reply(f"Argument is not entered in format. Example: 10sec/30min/1hour or 10s/30m/1h.")
        break
      
  await msg.reply(f"Ugh... fine, I'll remind you in {time} seconds.")
  await asyncio.sleep(time)
  
  if msg.from_user.id != msg.chat.id:
    # await bot.forward_message(msg.from_user.id, msg.chat.id, msg.id) # send pm
    return await bot.send_message(msg.chat.id, f"@{msg.from_user.username}, remind: {' '.join(arg[1:])}")
 
  return await bot.send_message(msg.chat.id, f"Remind: {' '.join(arg[1:])}")


@dp.message_handler(commands="note")
async def cmd_note(msg: types.Message):
  arg = msg.text.split()[1:]

  if not arg:
    return await msg.reply("Usage: /note <add/list/delete> <note>")
  
  if not data['notes'].get(str(msg.chat.id)):
    data['notes'][str(msg.chat.id)] = []

  if arg[0] == "add":
    if len(arg) == 1:
      return await msg.reply("Nothing to note here...")
    data['notes'][str(msg.chat.id)].append(" ".join(arg[1:]))
    return await msg.reply("Note succesfully created.")

  elif arg[0] == "list":
    if not data['notes'][str(msg.chat.id)]:
      return await msg.reply("You have no data['notes'], to create new: /note add <note>")
    answer = "*Note List*\n"
    for i in range(0, len(data['notes'][str(msg.chat.id)])):
      answer += f"{i+1}. {data['notes'][str(msg.chat.id)][i]}\n"
    return await msg.reply(answer, parse_mode = 'Markdown')
    
  elif arg[0] == "delete":
    if arg[1].isdigit():
      if int(arg[1]) == 0 or int(arg[1])-1 > len(data['notes'][str(msg.chat.id)]):
        return await msg.reply("That note already doesn't exists.")
      del data['notes'][str(msg.chat.id)][int(arg[1])-1]
      return await msg.reply("Note succesfully deleted.")
    elif arg[1] == "all":
      data['notes'][str(msg.chat.id)].clear()
      return await msg.reply("All notes was deleted.")
    else:
      return await msg.reply("Usage: /note delete <number/\"all\">")

  else:
    return await msg.reply("Usage: /note <add/list/delete> <note>")


@dp.message_handler(commands="pussy")
async def cmd_pussy(msg: types.Message):
  if requests.get("https://cataas.com").status_code != 200:
    return await bot.send_photo(msg.chat.id, IMG.open("data/cat.jpg"), "Something went wrong, so I draw this for you, baka!")

  arg = msg.text.split()[1:]
  res = "Here, take it, pervert!"

  if not arg:
    req = requests.get('https://cataas.com/c')
    if random.random() <= 0.25:
      res += " <span class=\"tg-spoiler\">Also try \"pussy help\"!</span>"
  else:
    if arg[0] == "help":
      return await bot.reply_to(msg,
      "\n\nCat with a text: _/pussy say <text>_"
      "\nCat with a tag: _/pussy <tag>_"
      "\nCat with a tag and text: _/pussy <tag> <text>_"
      "\n\nYou also can use advanced options by url: _/pussy url <url>_"
      "\nExample: _/pussy url gif/s/Hello?fi=sepia&c=orange&s=40&t=or_"
      "\n\nAll tags you can find here: [*click me*](https://cataas.com/api/tags)",
      parse_mode = "Markdown")
    elif arg[0] == "say":
      if len(arg) == 1:
        return await msg.reply("Nothing was found to say!")
      else:
        req = requests.get(f'https://cataas.com/c/s/{" ".join(arg[1:])}')
    elif arg[0] == "url":
      req = requests.get(f'https://cataas.com/c/{" ".join(arg[1:])}')
    else:
      if len(arg) == 1:
        req = requests.get(f'https://cataas.com/c/{arg[0]}')
      else:
        req = requests.get(f'https://cataas.com/c/{arg[0]}/s/{" ".join(arg[1:])}')
  
  if req.headers.get('Content-Type') == "image/gif":
    file_name = int(time.time())
    file = open(f"cache/{file_name}.gif", "wb")
    file.write(req.content)
    file.close()
    file = open(f"cache/{file_name}.gif", "rb")
    await bot.send_animation(msg.chat.id, file, caption=res, parse_mode="HTML")
    file.close()
    os.remove(f"cache/{file_name}.gif")
    return
  else:
    return await bot.send_photo(msg.chat.id, req.content, caption=res, parse_mode="HTML")


@dp.message_handler(commands="repeat")
async def cmd_repeat(msg: types.Message):
  arg = msg.text.split()[1:]  
  
  if not arg:
    return await msg.reply("Usage: /repeat <count> <message>")

  try:
    count = int(arg[0])
  except:
    return await msg.reply("Argument isn't number.")
  
  if count < 0:
    return await msg.reply("Argument isn't positive.")

  for _ in range(count):
    await bot.send_message(msg.chat.id, ' '.join(arg[1:]))
  
  return


@dp.message_handler()
async def get_mention(msg: types.Message):
  me = await bot.get_me()
  if msg.text == me.username:
    await msg.reply("https://github.com/LamberKeep/JoseeTelegram")


if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)
