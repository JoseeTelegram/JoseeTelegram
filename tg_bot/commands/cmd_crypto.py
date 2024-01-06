import math

import requests
from aiogram import types


async def cmd_crypto(msg: types.Message) -> None:
    answer = await msg.reply('Please wait...')
    res = "*Popular cryptocurrencies*\n"
    crypto = open("tg_bot/data/crypto.json", "r").read().json()
    for i in crypto:
        # print("Requesting:", i) # debug
        req = requests.get(f'https://data.messari.io/api/v1/assets/{i}/metrics').json()['data']['market_data']
        res += f"*{crypto[i]['name']} ({crypto[i]['short-name']})* - ${RoundTo(req['price_usd'])}"
        if req['percent_change_usd_last_1_hour']:   res += f" (1h: {RoundTo(req['percent_change_usd_last_1_hour'])}%"
        if req['percent_change_usd_last_24_hours']:
            res += f" 24h: {RoundTo(req['percent_change_usd_last_24_hours'])}%)"
        else:
            if req['percent_change_usd_last_1_hour']: res += ")"
        res += "\n"
    await msg.bot.edit_message_text(res, msg.chat.id, answer.message_id, parse_mode='Markdown')
    return


def RoundTo(num, digits=2):
    if num == 0:
        return 0
    scale = int(-math.floor(math.log10(abs(num - int(num))))) + digits - 1
    if scale < digits:
        scale = digits
    return round(num, scale)
