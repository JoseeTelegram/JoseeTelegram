import math
import os
from time import time

from aiogram import types
from josee import bot
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
    IMG.new("RGB", (128, 128), (r, g, b)).save(f"tg_bot/cache/{file_name}.png", bitmap_format="png")
    file = open(f"tg_bot/cache/{file_name}.png", "rb")
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

  os.remove(f"tg_bot/cache/{file_name}.png")
  return file.close()



def rgb2hex(r:int, g:int, b:int):
  if 0 < r > 255 or 0 < g > 255 or 0 < b > 255: 
    return False

  return "%02x" % r, "%02x" % g, "%02x" % b 

def rgb2hsv(r:int, g:int, b:int):
  if 0 < r > 255 or 0 < g > 255 or 0 < b > 255: 
    return False

  r /= 255
  g /= 255
  b /= 255

  M = max(r, g, b)
  m = min(r, g, b)

  diff = M - m

  h = -1
  if (M == m):
    h = 0
  elif (M == r):
    h = (60 * ((g - b) / diff) + 360) % 360
  elif (M == g):
    h = (60 * ((b - r) / diff) + 120) % 360
  elif (M == b):
    h = (60 * ((r - g) / diff) + 240) % 360

  s = 0
  if M != 0:
    s = (diff / M) * 100

  v = M * 100

  return h, s, v

def hsv2rgb(h: int, s: int, v: int):
  if 0 < h > 360 or 0 < s > 100 or 0 < v > 100: 
    return False

  s = s / 100
  v = v / 100

  c = s * v
  x = c * (1 - abs(math.fmod(h / 60, 2) - 1))
  m = v - c

  if 0 >= h < 60:
    r = 0
    g = x
    b = c
  elif 60 >= h < 120:
    r = 0
    g = c
    b = x
  elif 120 >= h < 180:
    r = x
    g = c
    b = 0
  elif 180 >= h < 240:
    r = c
    g = x
    b = 0
  elif 240 >= h < 300:
    r = c
    g = 0
    b = x
  else:
    r = x
    g = 0
    b = c

  r = (r + m) * 255
  g = (g + m) * 255
  b = (b + m) * 255

  return r, g, b


def rgb2cmyk(r:int, g:int, b:int):
  if 0 < r > 255 or 0 < g > 255 or 0 < b > 255: 
    return False

  r /= 255
  g /= 255
  b /= 255

  k = 1 - max(r, g, b)

  return (1 - r - k) / (1 - k) * 100, (1 - g - k) / (1 - k) * 100, (1 - b - k) / (1 - k) * 100, k * 100  

def get_rainbow(count: int):
  if count <= 0: return False
  rainbow = []
  diff = int(360 / count)
  for i in range(count):
    color = list(round(j) for j in hsv2rgb(diff*i, 100, 100))
    rainbow.append('#' + ''.join(rgb2hex(color[0], color[1], color[2])))
  return rainbow

def main():
  print(get_rainbow(3))

if __name__ == "__main__":
  main()
