import platform
from time import time

import psutil
import requests
from aiogram import types
from josee import start_time


async def cmd_sysfetch(msg: types.Message) -> None:
  up_time = getReadableTime(round(time() - start_time))
  await msg.reply(
  f"<b>Platform:</b> {platform.system()} {platform.release()}\n"
  f"<b>Architecture:</b> {platform.machine()}\n"
  f"<b>Uptime:</b> {up_time[0]} days {up_time[1]} hours {up_time[2]} mins {up_time[3]} secs\n"
  f"<b>CPU:</b> {round(psutil.cpu_freq()[0]*1000)}/{round(psutil.cpu_freq()[2])} GHz ({round(psutil.cpu_percent())}%)\n"
  f"<b>RAM:</b> {round(psutil.virtual_memory().used / (1024.0 * 2))}/{round(psutil.virtual_memory().total / (1024.0 * 2))} MB ({round(psutil.virtual_memory().percent)}%)\n"
  f"<b>IP:</b> {requests.get('http://icanhazip.com').text.rstrip()}\n", 'HTML')
  return

def getReadableTime(seconds: int):
  if seconds <= 0: return False

  days = 0
  hours = 0
  minutes = 0

  while seconds >= 60:
    if seconds >= 86400:
      days += 1
      time -= 86400
    elif seconds >= 3600:
      hours += 1
      seconds -= 3600
    else:
      minutes += 1
      seconds -= 60

  return days, hours, minutes, seconds

if __name__ == "__main__": # test
    time = getReadableTime(1000) # 16 min 40 sec
    print(f"{time[0]} days {time[1]} hours {time[2]} mins {time[3]} secs")
