import random

from aiogram import types
from aiogram.types import Message
from aiogram.utils.emoji import emojize


async def cmd_coin(msg: types.Message) -> Message:
    return await msg.reply(emojize(f"You get a "
                                   f"{['Head! :full_moon_with_face:', 'Tail! :new_moon_with_face:'][random.randint(0, 1)]}"))
