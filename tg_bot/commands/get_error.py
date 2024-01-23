import logging


async def get_error(update, exception) -> None:
    logging.exception(exception)
    logging.debug(update)

    return
