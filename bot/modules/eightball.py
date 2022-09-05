import random

from aiogram import types
from josee import data


async def cmd_8ball(msg: types.Message) -> None:
  await msg.reply(random.choice(data['8ball']))
  return
