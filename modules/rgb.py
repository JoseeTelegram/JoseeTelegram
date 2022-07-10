import os
from time import time

from aiogram import types
from josee import bot
from libs.colors import *
from PIL import Image as IMG


async def cmd_rgb(msg: types.Message) -> None:
  arg = msg.text.split()[1:]

  if not arg:
    await msg.reply("Usage: /rgb <r> <g> <b>")
    return

  r = int(arg[0])
  g = int(arg[1])
  b = int(arg[2])

  try:
    file_name = int(time())
    IMG.new("RGB", (128, 128), (r, g, b)).save(f"cache/{file_name}.png", bitmap_format="png")
    file = open(f"cache/{file_name}.png", "rb")
  except Exception as e:
    print(e)
    await msg.reply("Error, usage: /rgb <r> <g> <b>")
    return

  await bot.send_photo(msg.chat.id, file,
  f"*RGB:* {r}, {g}, {b}\n"
  f"*HEX:* #{''.join(str(i) for i in rgb2hex(r, g, b))}\n"
  f"*HSV:* {', '.join(str(round(i)) for i in rgb2hsv(r, g, b))}\n"
  f"*CMYK:* {', '.join(str(round(i)) for i in rgb2cmyk(r, g, b))}\n",
  parse_mode = "Markdown")

  os.remove(f"cache/{file_name}.png")
  return file.close()
