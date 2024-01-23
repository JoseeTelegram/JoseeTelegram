import logging

from aiogram import types
from aiogram.types import Message
from translatepy import Translator

translator = Translator()


async def cmd_translate(msg: types.Message) -> Message:
    args = msg.text.split()

    if len(args) <= 1:
        return await msg.reply("Usage: /translate <language> <message>\nOn reply: /translate <language>")

    lang = args[1]

    logging.info(len(args))

    if len(args) > 2:
        message = ' '.join(args[2:])
    elif msg.reply_to_message.text:
        message = msg.reply_to_message.text
    else:
        return await msg.reply("No message")

    return await msg.reply(translator.translate(message, lang).result)
