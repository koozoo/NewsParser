import logging

from aiogram import Dispatcher, Bot

from settings.config import settings
from bot.handlers import register_handlers
from scheduler.main import scheduler
from services.main import Service
from services.telegram_parser.main import client as telegram_parser
from settings.prompt import prompt
from logging_.main import setup_logging


async def _register_all_handlers(dp: Dispatcher):
    await register_handlers(dp=dp)


async def _register_global_task(**kwarg):
    service_entity = Service()

    scheduler.add_job(func=service_entity.init_parsing, trigger="cron", minute="*/1", kwargs={"type_": "telegram"})
    scheduler.add_job(func=service_entity.init_open_ai, trigger="cron", minute="*/1")
    scheduler.add_job(func=service_entity.init_approve_notification, trigger="cron", minute="*/1",
                      kwargs={"bot": kwarg['bot']})
    # scheduler.add_job(func=service_entity.init_parsing, trigger="cron", minute="*/1", kwargs={"type_": "web"})


async def _run_all_sub_services():
    await telegram_parser.start()
    scheduler.start()


async def set_config():
    await prompt()


async def start_bot():
    # await setup_logging()
    bot = Bot(token=settings.bot.token, parse_mode='HTML')

    dp = Dispatcher()
    await _register_all_handlers(dp=dp)
    await _register_global_task(dp=dp, bot=bot)
    await set_config()
    dp.startup.register(_run_all_sub_services)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.info(f"{e}")
        await dp.stop_polling()
