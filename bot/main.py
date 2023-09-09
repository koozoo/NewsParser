from aiogram import Dispatcher, Bot

import settings as config


async def register_all_handlers(dp: Dispatcher):
    ...


async def _run_global_task():
    ...


async def start_bot():
    bot = Bot(token=config.settings.bot.token, parse_mode='HTML')
    dp = Dispatcher()
    dp.startup.register(_run_global_task)
