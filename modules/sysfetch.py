import platform
from time import time

import psutil
import requests
from aiogram import types
from josee import start_time
from libs.time import getReadableTime


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
