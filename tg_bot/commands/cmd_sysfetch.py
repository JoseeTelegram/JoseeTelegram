import platform
from time import time

import psutil
import requests
from aiogram import types

start_time = time()


async def cmd_sysfetch(msg: types.Message) -> None:
    up_time = getReadableTime(round(time() - start_time))
    await msg.reply(
        f"<b>{' System Information ':─^30}</b>"
        f"\n<b>Platform:</b> {platform.system()} {platform.release()}"
        f"\n<b>Architecture:</b> {platform.machine()}"
        f"\n<b>Uptime:</b> {up_time[0]}d {up_time[1]}h {up_time[2]}m {up_time[3]}s"
        f"\n<b>CPU:</b> {round(psutil.cpu_freq()[0])}/{round(psutil.cpu_freq()[2])} GHz ({round(psutil.cpu_percent())}%)"
        f"\n<b>RAM:</b> {round(psutil.virtual_memory().used / 1024 ** 2)}/{round(psutil.virtual_memory().total / 1024 ** 2)} MB ({round(psutil.virtual_memory().percent)}%)"
        f"\n<b>IP:</b> {requests.get('http://icanhazip.com').text.rstrip()}"
        f"\n<b>{' System Information ':─^30}</b>"
        , 'HTML')
    return


def getReadableTime(seconds: int):
    if seconds <= 0:
        return False

    days = seconds // 86400
    seconds -= 86400 * days
    hours = seconds // 3600
    seconds -= 3600 * hours
    minutes = seconds // 60
    seconds -= 60 * minutes

    return days, hours, minutes, seconds
