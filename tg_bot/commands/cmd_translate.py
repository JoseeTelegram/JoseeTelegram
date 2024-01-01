from aiogram import types
from translatepy import Translator

translator = Translator()

async def cmd_translate(msg: types.Message) -> None:
  args = msg.text.split()

  if len(args) <= 1:
    return await msg.reply("Usage: /translate <language> <message>")

  lang = args[1]
  message = ' '.join(args[2:])
  return await msg.reply(translator.translate(message, lang))