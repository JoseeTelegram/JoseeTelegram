import os
import random
from time import time

import requests
from aiogram import types
from josee import tg_bot
from PIL import Image as IMG


async def cmd_pussy(msg: types.Message) -> None:
  if requests.get("https://cataas.com").status_code != 200:
    await tg_bot.send_photo(msg.chat.id, IMG.open("data/cat.jpg"), "Something went wrong, so I draw this for you, baka!")
    return

  arg = msg.text.split()[1:]
  res = "Here, take it, pervert!"

  if not arg:
    req = requests.get('https://cataas.com/c')
    if random.random() <= 0.25:
      res += " <span class=\"tg-spoiler\">Also try \"pussy help\"!</span>"
  else:
    if arg[0] == "help":
      await tg_bot.reply_to(msg,
      "\n\nCat with a text: _/pussy say <text>_"
      "\nCat with a tag: _/pussy <tag>_"
      "\nCat with a tag and text: _/pussy <tag> <text>_"
      "\n\nYou also can use advanced options by url: _/pussy url <url>_"
      "\nExample: _/pussy url gif/s/Hello?fi=sepia&c=orange&s=40&t=or_"
      "\n\nAll tags you can find here: [*click me*](https://cataas.com/api/tags)",
      parse_mode = "Markdown")
      return
    elif arg[0] == "say":
      if len(arg) == 1:
        await msg.reply("Nothing was found to say!")
        return
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
    file_name = int(time())
    file = open(f"cache/{file_name}.gif", "wb")
    file.write(req.content)
    file.close()
    file = open(f"cache/{file_name}.gif", "rb")
    await tg_bot.send_animation(msg.chat.id, file, caption=res, parse_mode="HTML")
    file.close()
    os.remove(f"cache/{file_name}.gif")
    return
  else:
    await tg_bot.send_photo(msg.chat.id, req.content, caption=res, parse_mode="HTML")
    return
