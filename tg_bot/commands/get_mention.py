from aiogram import types


async def get_mention(msg: types.Message) -> None:
    me = await msg.bot.get_me()

    if msg.text == f"@{me.username}":
        await msg.reply("https://github.com/LamberKeep/JoseeTelegram")