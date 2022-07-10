from aiogram import Dispatcher

from .cat import cmd_cat
from .coin import cmd_coin
from .crypto import cmd_crypto
from .eightball import cmd_8ball
from .mention import get_mention
from .note import cmd_note
from .pussy import cmd_pussy
from .random import cmd_random
from .remind import cmd_remind
from .repeat import cmd_repeat
from .rgb import cmd_rgb
from .sysfetch import cmd_sysfetch


def setup(dp: Dispatcher):
  dp.register_message_handler(cmd_cat, commands="cat")
  dp.register_message_handler(cmd_coin, commands="coin")
  dp.register_message_handler(cmd_crypto, commands="crypto")
  dp.register_message_handler(cmd_8ball, commands="8ball")
  dp.register_message_handler(cmd_note, commands="note")
  dp.register_message_handler(cmd_pussy, commands="pussy")
  dp.register_message_handler(cmd_random, commands="random")
  dp.register_message_handler(cmd_remind, commands="remind")
  dp.register_message_handler(cmd_repeat, commands="repeat")
  dp.register_message_handler(cmd_rgb, commands="rgb")
  dp.register_message_handler(cmd_sysfetch, commands="sysfetch")
  dp.register_message_handler(get_mention)
