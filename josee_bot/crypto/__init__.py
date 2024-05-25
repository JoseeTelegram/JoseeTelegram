import asyncio
import json
import logging

import requests

logger = logging.getLogger(__name__)

while True:
    print("Refreshing crypto data...")
    # logger.info("Refreshing crypto data...")
    crypto = open(file="tg_bot/data/crypto.json", mode="r+")
    data = json.loads(crypto.read())
    for i in data:
        data[i] = requests.get(f'https://data.messari.io/api/v1/assets/{i}/metrics').json()
    crypto.flush()
    crypto.write(json.dumps(data))
    crypto.close()
    asyncio.sleep(crypto_update)
