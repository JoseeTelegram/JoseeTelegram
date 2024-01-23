import random

from aiogram import types


async def cmd_random(msg: types.Message) -> None:
    arg = msg.text.split()[1:]

    if not arg:
        await msg.reply("Usage: /random <start> <end>")
        return

    try:
        start = int(arg[0])
        if len(arg) == 1:
            await msg.reply(str(random.randrange(0, start)))
            return
        end = int(arg[1])
        if start < end:
            await msg.reply(str(random.randrange(start, end)))
            return
        elif start == end:
            await msg.reply("Both integers are the same.")
            return
        else:
            await msg.reply(str(random.randrange(end, start)))
            return
    except ValueError:
        await msg.reply(f"One of the arguments isn\'t an integer.")
        return
