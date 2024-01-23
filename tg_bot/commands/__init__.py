from aiogram import Dispatcher

from .cmd_cat import cmd_cat
from .cmd_coin import cmd_coin
from .cmd_crypto import cmd_crypto
from .cmd_dice import cmd_dice
from .cmd_eightball import cmd_8ball
from .cmd_note import cmd_note
from .cmd_pussy import cmd_pussy
from .cmd_random import cmd_random
from .cmd_remind import cmd_remind
from .cmd_repeat import cmd_repeat
from .cmd_rgb import cmd_rgb
from .cmd_sysfetch import cmd_sysfetch
from .cmd_translate import cmd_translate
from .get_error import get_error
from .get_mention import get_mention


def setup(dp: Dispatcher):
    dp.register_message_handler(cmd_cat, commands="cat")
    dp.register_message_handler(cmd_coin, commands="coin")
    dp.register_message_handler(cmd_crypto, commands="crypto")
    dp.register_message_handler(cmd_dice, commands="dice")
    dp.register_message_handler(cmd_8ball, commands="8ball")
    dp.register_message_handler(cmd_note, commands="note")
    dp.register_message_handler(cmd_pussy, commands="pussy")
    dp.register_message_handler(cmd_random, commands="random")
    dp.register_message_handler(cmd_remind, commands="remind")
    dp.register_message_handler(cmd_repeat, commands="repeat")
    dp.register_message_handler(cmd_rgb, commands="rgb")
    dp.register_message_handler(cmd_sysfetch, commands="sysfetch")
    dp.register_message_handler(cmd_translate, commands="translate")
    dp.register_message_handler(get_mention)
    dp.register_errors_handler(get_error)
