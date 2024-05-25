import asyncio
import platform
import random
from io import BytesIO
from time import ctime
from time import time

import emoji
import psutil
import requests
from PIL import Image as IMG
from aiogram import Bot, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, URLInputFile, BufferedInputFile
from loguru import logger
from translatepy import Translator

from josee_bot import EIGHT_BALL, CRYPTO
from josee_bot.misc import dp


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(Command("echo"))
async def cmd_echo(msg: Message) -> None:
    res = msg.text[5:]
    if res:
        await msg.bot.send_message(msg.chat.id, res)


@dp.message(Command("coin"))
async def cmd_coin(msg: Message) -> None:
    await msg.reply(emoji.emojize(f"You get a "
                                  f"{['Head! :full_moon_with_face:', 'Tail! :new_moon_with_face:']
                                  [random.randint(0, 1)]}", language='alias'))


@dp.message(Command("crypto"))
async def cmd_crypto(msg: Message) -> None:
    request = requests.get("https://bitpay.com/api/rates")

    if request.status_code != 200 or request.headers.get("Content-Type") != "application/json; charset=utf-8":
        await msg.reply("The service is currently unavailable, please try again later.")
        return

    response = request.json()
    result = "*Cryptocurrency rates*"

    usd_price = float(filter_crypto_rate(response, "USD")['rate'])  # BTC price in USD

    for i in CRYPTO:
        code = i.strip("\n")
        crypto = filter_crypto_rate(response, code)
        result += f"\n{crypto['name']} ({code}) - {round(usd_price / float(crypto['rate']), 3)} $"

    await msg.reply(result, parse_mode='Markdown')


def filter_crypto_rate(crypto_rates: list, name: str) -> dict | None:
    for crypto_rate in crypto_rates:
        if crypto_rate["code"] == name.upper():
            return crypto_rate


@dp.message(Command("dice"))
async def cmd_dice(msg: Message) -> None:
    arg = msg.text.split()[1:]

    if not arg:
        await msg.reply("Usage: /dice <edges> <number>", parse_mode="markdown")
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
        emoji.emojize(f":game_die: {msg.from_user.username} rolled {nDice}d{nSides} and got {nTotal}",
                      language="alias"))


@dp.message(Command("8ball"))
async def cmd_8ball(msg: Message) -> None:
    await msg.reply(emoji.emojize(f":8ball: {random.choice(EIGHT_BALL)}", language="alias"))


note = {}


@dp.message(Command("note"))
async def cmd_note(msg: Message) -> None:
    arg = msg.text.split()[1:]

    if not arg:
        await msg.reply("Usage: /note <add/list/delete> <note>", parse_mode="markdown")
        return

    notes = open("tg_bot/data/notes.json", "r+")

    if notes.read == "":
        notes.write("{}")

    if arg[0] == "add":
        if len(arg) == 1:
            await msg.reply("Nothing to note here...")
            return

        note[str(msg.chat.id)].append(" ".join(arg[1:]))
        await msg.reply("Note succesfully created.")

    elif arg[0] == "list":
        if not note[str(msg.chat.id)]:
            await msg.reply("You have no notes, to create new: /note add <note>")
            return

        answer = "*Note List*\n"

        for i in range(0, len(note[str(msg.chat.id)])):
            answer += f"{i + 1}. {note[str(msg.chat.id)][i]}\n"

        await msg.reply(answer, parse_mode='Markdown')

    elif arg[0] == "delete":
        if arg[1].isdigit():
            if int(arg[1]) == 0 or int(arg[1]) - 1 > len(note[str(msg.chat.id)]):
                await msg.reply("That note already doesn't exists.")
                return
            del note[str(msg.chat.id)][int(arg[1]) - 1]
            await msg.reply("Note succesfully deleted.")
        elif arg[1] == "all":
            note[str(msg.chat.id)].clear()
            await msg.reply("All notes was deleted.")
        else:
            await msg.reply("Usage: /note delete <number/\"all\">", parse_mode="markdown")

    else:
        await msg.reply("Usage: /note <add/list/delete> <note>", parse_mode="markdown")


@dp.message(Command("cat"))
async def cmd_cat(msg: Message) -> None:
    request = requests.get('https://cataas.com/cat?json=true')  # Get a random cat

    if request.status_code == 200 and request.headers.get("Content-Type") == "application/json; charset=utf-8":
        response = request.json()
        cat_id = response["_id"]
        cat_mimetype = response["mimetype"].split("/")[-1]

        if cat_id and cat_mimetype:
            cat_filename = cat_id + "." + cat_mimetype

            if cat_mimetype == "jpeg" or cat_mimetype == "png":
                await msg.reply_photo(
                    photo=URLInputFile(f"https://cataas.com/cat/{cat_id}", filename=cat_filename))
            elif cat_mimetype == "gif":
                await msg.reply_animation(
                    animation=URLInputFile(f"https://cataas.com/cat/{cat_id}", filename=cat_filename))
            else:
                await msg.reply_document(
                    document=URLInputFile(f"https://cataas.com/cat/{cat_id}", filename=cat_filename))

            return

    await msg.reply(emoji.emojize("Ops! Oh! Something went wrong, please try again later :crying_cat_face:",
                                  language="alias"))


@dp.message(Command("random"))
async def cmd_random(msg: Message) -> None:
    arg = msg.text.split()[1:]

    if not arg:
        await msg.reply("Usage: /random <start> <end>", parse_mode="markdown")
        return

    try:
        start = int(arg[0])

        if len(arg) == 1:
            await msg.reply(str(random.randrange(0, start)))
            return

        end = int(arg[1])

        if start < end:
            await msg.reply(str(random.randrange(start, end)))
        elif start == end:
            await msg.reply("Both integers are the same.")
        else:
            await msg.reply(str(random.randrange(end, start)))
    except ValueError:
        await msg.reply(f"One of the arguments isn\'t an integer.")


@dp.message(Command("remind"))
async def cmd_remind(msg: Message) -> None:
    global arg_time
    arg = msg.text.split()[1:]

    if not arg:
        await msg.reply("Usage: /remind <time> <message>", parse_mode="markdown")
        return

    if arg[0].isdigit():
        arg_time = int(arg[0])
    else:
        if not arg[0][0].isdigit():
            await msg.reply("Argument doesn't contain a number.")
            return

        for sym in range(0, len(arg[0])):
            if not arg[0][sym].isdigit():
                arg_time = int(arg[0][:sym])

                if arg[0][sym:] in ["sec", "s"]:
                    pass
                elif arg[0][sym:] in ["min", "m"]:
                    arg_time *= 60
                elif arg[0][sym:] in ["hour", "h"]:
                    arg_time *= 3600
                else:
                    await msg.reply(f"Argument is not entered in format. Example: 10sec/30min/1hour or 10s/30m/1h.")
                    return
                break

    await msg.reply(f"Ugh... fine, I'll remind you in {arg_time} sec.")
    await asyncio.sleep(arg_time)

    message = ""

    if len(arg) > 1:
        message = f"\nMessage: \"{' '.join(arg[1:])}\""

    if msg.chat.type == "supergroup":
        await Bot.send_message(msg.from_user.id,
                               f'Remind from <u><a href="https://t.me/{msg.chat.username}">{msg.chat.title}</a></u>.{message}',
                               parse_mode="HTML")
        await msg.answer(f"@{msg.from_user.username}\nRemind at {ctime(time() - arg_time)}.{message}")
        return

    await msg.answer(f"Remind at {ctime(time() - arg_time)}.{message}")
    return


@dp.message(Command("repeat"))
async def cmd_repeat(msg: Message) -> None:
    arg = msg.text.split()[1:]

    if not arg:
        await msg.reply("Usage: /repeat <count> <message>", parse_mode="markdown")
        return

    try:
        count = int(arg[0])
    except ValueError:
        await msg.reply("Argument isn't number.")
        return

    if count < 0:
        await msg.reply("Argument isn't positive.")
        return

    for _ in range(count):
        await msg.answer(' '.join(arg[1:]))


@dp.message(Command("rgb"))
async def cmd_rgb(msg: Message) -> None:
    usage = "Usage: /rgb <r> <g> <b>"
    arg = msg.text.split()[1:]

    if not arg:
        await msg.reply(usage, parse_mode="markdown")
        return

    r = int(arg[0])
    g = int(arg[1])
    b = int(arg[2])

    if 0 < r > 255 or 0 < g > 255 or 0 < b > 255:
        await msg.reply(usage, parse_mode="markdown")
        return

    buffer = BytesIO()
    IMG.new("RGB", (128, 128), (r, g, b)).save(buffer, format="PNG")
    buffer.seek(0)

    await msg.reply_photo(photo=BufferedInputFile(buffer.read(), filename="color.png"),
                          caption=f"*RGB:* {r}, {g}, {b}\n"
                                  f"*HEX:* #{''.join(str(i) for i in rgb2hex(r, g, b))}\n"
                                  f"*HSV:* {', '.join(str(round(i)) for i in rgb2hsv(r, g, b))}\n"
                                  f"*CMYK:* {', '.join(str(round(i)) for i in rgb2cmyk(r, g, b))}\n",
                          parse_mode="Markdown")


def rgb2hex(r: int, g: int, b: int):
    return "%02x" % r, "%02x" % g, "%02x" % b


def rgb2hsv(r: int, g: int, b: int):
    if 0 < r > 255 or 0 < g > 255 or 0 < b > 255:
        return False

    r /= 255
    g /= 255
    b /= 255

    M = max(r, g, b)
    m = min(r, g, b)

    diff = M - m

    h = -1

    if M == m:
        h = 0
    elif M == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif M == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    elif M == b:
        h = (60 * ((r - g) / diff) + 240) % 360

    s = 0

    if M != 0:
        s = (diff / M) * 100

    v = M * 100

    return h, s, v


def rgb2cmyk(r: int, g: int, b: int):
    r /= 255
    g /= 255
    b /= 255

    k = 1 - max(r, g, b)

    return (1 - r - k) / (1 - k) * 100, (1 - g - k) / (1 - k) * 100, (1 - b - k) / (1 - k) * 100, k * 100


start_time = time()


@dp.message(Command("sysfetch"))
async def cmd_sysfetch(msg: Message) -> None:
    up_time = getReadableTime(round(time() - start_time))

    await msg.reply(
        f"<b>{' System Information ':─^30}</b>"
        f"\n<b>Platform:</b> {platform.system()} {platform.release()}"
        f"\n<b>Architecture:</b> {platform.machine()}"
        f"\n<b>Uptime:</b> {up_time[0]}d {up_time[1]}h {up_time[2]}m {up_time[3]}s"
        f"\n<b>CPU:</b> {round(psutil.cpu_freq()[0])}/{round(psutil.cpu_freq()[2])} GHz ({round(psutil.cpu_percent())}%)"
        f"\n<b>RAM:</b> {round(psutil.virtual_memory().used / 1024 ** 2)}/{round(psutil.virtual_memory().total / 1024 ** 2)} MB ({round(psutil.virtual_memory().percent)}%)"
        f"\n<b>IP:</b> {requests.get('http://icanhazip.com').text.rstrip()}"
        f"\n<b>{' System Information ':─^30}</b>"
        , 'HTML')

    return


def getReadableTime(seconds: int):
    if seconds <= 0:
        return False

    days = seconds // 86400
    seconds -= 86400 * days
    hours = seconds // 3600
    seconds -= 3600 * hours
    minutes = seconds // 60
    seconds -= 60 * minutes

    return days, hours, minutes, seconds


translator = Translator()


@dp.message(Command("translate"))
async def cmd_translate(msg: Message) -> None:
    args = msg.text.split()

    if len(args) <= 1:
        await msg.reply("Usage: /translate <language> <message>\nOn reply: /translate <language>",
                        parse_mode="markdown")
        return

    lang = args[1]

    logger.info(len(args))

    if len(args) > 2:
        message = ' '.join(args[2:])
    elif msg.reply_to_message.text:
        message = msg.reply_to_message.text
    else:
        await msg.reply("No message")
        return

    await msg.reply(translator.translate(message, lang).result)
