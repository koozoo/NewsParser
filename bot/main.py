import logging

from aiogram import Dispatcher, Bot

import settings as config
from bot.handlers import register_handlers
from scheduler.main import scheduler


async def register_all_handlers(dp: Dispatcher):
    await register_handlers(dp=dp)


async def _run_global_task():
    print(scheduler)


async def start_bot():
    # init logging
    bot = Bot(token=config.settings.bot.token, parse_mode='HTML')

    dp = Dispatcher()
    await register_all_handlers(dp=dp)

    dp.startup.register(_run_global_task)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.info(f"{e}")
        await dp.stop_polling()
