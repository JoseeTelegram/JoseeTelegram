from aiogram import types


async def cmd_cat(msg: types.Message) -> None:
  res = msg.text[5:]
  if res: 
    await msg.bot.send_message(msg.chat.id, res)
    return
