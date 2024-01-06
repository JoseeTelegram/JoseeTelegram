from aiogram import types
from aiogram.types import Message


async def cmd_cat(msg: types.Message) -> Message:
  res = msg.text[5:]
  if res:
    return await msg.bot.send_message(msg.chat.id, res)
