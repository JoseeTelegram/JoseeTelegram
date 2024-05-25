import logging
import sys

from josee_bot import misc
from josee_bot.handlers.base import *


async def main() -> None:
    await misc.setup()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
