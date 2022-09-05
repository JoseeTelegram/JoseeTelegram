from aiogram import types
from josee import bot


async def get_mention(msg: types.Message) -> None:
  me = await bot.get_me()
  # print(f'msg.text: \t{msg.text}\nbot.get_me(): \t{me.username}')
  if msg.text == f"@{me.username}":
    await msg.reply("https://github.com/LamberKeep/JoseeTelegram")
