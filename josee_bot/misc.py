from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger

from josee_bot import config

bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def setup():
    logger.info("Configure handlers...")
    # noinspection PyUnresolvedReferences
    import josee_bot.handlers

    await dp.start_polling(bot)
