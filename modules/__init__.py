from aiogram import Dispatcher

from modules.cat import cmd_cat
from modules.coin import cmd_coin
from modules.crypto import cmd_crypto
from modules.eightball import cmd_8ball
from modules.error import get_error
from modules.mention import get_mention
from modules.note import cmd_note
from modules.pussy import cmd_pussy
from modules.random import cmd_random
from modules.remind import cmd_remind
from modules.repeat import cmd_repeat
from modules.rgb import cmd_rgb
from modules.sysfetch import cmd_sysfetch


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
  dp.register_errors_handler(get_error)
