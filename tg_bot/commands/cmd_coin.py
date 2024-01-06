import random

from aiogram import types
from aiogram.types import Message


async def cmd_coin(msg: types.Message) -> Message:
    return await msg.reply(f"You get a {['Head! 🌝', 'Tail! 🌚'][random.randint(0, 1)]}")
