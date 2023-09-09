import logging
from datetime import datetime

from bot.database.main import async_session_maker


async def add_item(obj):
    async with async_session_maker() as s:
        async with s.begin():
            s.add(obj)
            await s.commit()
            logging.info(f"item add in data base {datetime.now()}")


async def add_item_autoincrement(obj):
    async with async_session_maker() as s:

        s.add(obj)
        await s.flush()

        await s.commit()

        logging.info(f"item add in data base {datetime.now()}")
        return int(obj.id)


async def add_transaction_autoincrement(lst_obj: list):
    async with async_session_maker() as s:

        s.add_all(lst_obj)
        await s.flush()

        await s.commit()

        logging.info(f"item add in data base {datetime.now()}")
