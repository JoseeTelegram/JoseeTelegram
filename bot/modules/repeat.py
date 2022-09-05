from aiogram import types
from josee import bot


async def cmd_repeat(msg: types.Message) -> None:
  arg = msg.text.split()[1:]  
  
  if not arg:
    await msg.reply("Usage: /repeat <count> <message>")
    return

  try:
    count = int(arg[0])
  except:
    await msg.reply("Argument isn't number.")
    return
  
  if count < 0:
    await msg.reply("Argument isn't positive.")
    return

  for _ in range(count):
    await bot.send_message(msg.chat.id, ' '.join(arg[1:]))
  return
