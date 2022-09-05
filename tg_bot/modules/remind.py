import asyncio
from time import ctime
from time import time as now

from aiogram import types
from josee import tg_bot


async def cmd_remind(msg: types.Message) -> None:
  arg = msg.text.split()[1:]

  if not arg:
    await msg.reply("Usage: /remind <time> <message>")
    return
  
  if arg[0].isdigit():
    time = int(arg[0])
  else:
    if not arg[0][0].isdigit():
      await msg.reply("Argument doesn't contain a number.")
      return
    for sym in range(0, len(arg[0])):
      if not arg[0][sym].isdigit():
        time = int(arg[0][:sym])
        if arg[0][sym:] in ["sec", "s"]:
          pass
        elif arg[0][sym:] in ["min", "m"]:
          time *= 60
        elif arg[0][sym:] in ["hour", "h"]:
          time *= 3600
        else:
          await msg.reply(f"Argument is not entered in format. Example: 10sec/30min/1hour or 10s/30m/1h.")
          return
        break
      
  await msg.reply(f"Ugh... fine, I'll remind you in {time} sec.")
  await asyncio.sleep(time)
  
  message = ""
  if len(arg) > 1:
    message = f"\nMessage: \"{' '.join(arg[1:])}\""

  if msg.chat.type == "supergroup":
    await tg_bot.send_message(msg.from_user.id,
    f'Remind from <u><a href="https://t.me/{msg.chat.username}">{msg.chat.title}</a></u>.{message}',
    parse_mode="HTML")
    await msg.answer(f"@{msg.from_user.username}\nRemind at {ctime(now()-time)}.{message}")
    return
 
  await msg.answer(f"Remind at {ctime(now()-time)}.{message}")
  return
