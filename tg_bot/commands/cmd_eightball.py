import random

from aiogram import types

results = [
    "Without a doubt."
    , "As I see it yes."
    , "Outlook not so good."
    , "Reply hazy ask again."
    , "Most likely."
    , "Ask again later."
    , "Don't count on it."
    , "Signs point to yes."
    , "My sources say no."
]


async def cmd_8ball(msg: types.Message) -> None:
    await msg.reply(random.choice(results))
    return
