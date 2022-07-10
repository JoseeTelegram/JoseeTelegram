import random

from aiogram import types


async def cmd_coin(msg: types.Message) -> None:
  await msg.reply(f"You get a {['Head', 'Tail'][random.randint(0,1)]}!")
  return
