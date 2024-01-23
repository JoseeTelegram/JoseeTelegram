import random

from aiogram import types
from aiogram.utils.emoji import emojize


async def cmd_dice(msg: types.Message) -> None:
    arg = msg.text.split()[1:]

    if not arg:
        await msg.reply("Usage: /dice <edges> <number>")
        return

    nDice = 1

    try:
        nSides = int(arg[0])

        if len(arg) > 1:
            nDice = int(arg[1])
    except ValueError:
        await msg.reply(f"One of the arguments isn\'t an integer.")
        return

    if nDice < 1:
        nDice = 1

    if nSides < 2:
        nSides = 2

    nTotal = 0

    for x in range(0, nDice):
        nTotal += random.randint(1, nSides)

    await msg.reply(
        emojize(f":game_die: {msg.from_user.username} rolled {nDice}d{nSides} and got {nTotal}"))
