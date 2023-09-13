import logging

from aiogram import Dispatcher, Bot

from settings.config import settings
from bot.handlers import register_handlers
from scheduler.main import scheduler
from services.main import Service
from services.telegram_parser.main import client as telegram_parser


async def register_all_handlers(dp: Dispatcher):
    await register_handlers(dp=dp)


async def _run_global_task():
    service_entity = Service()

    scheduler.add_job(func=service_entity.init_parsing, trigger="cron", minute="*/1", kwargs={"type_": "telegram"})
    # scheduler.add_job(func=service_entity.init_parsing, trigger="cron", minute="*/1", kwargs={"type_": "web"})
    await _run_all_sub_services()


async def _run_all_sub_services():
    await telegram_parser.start()
    scheduler.start()


async def start_bot():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
    bot = Bot(token=settings.bot.token, parse_mode='HTML')

    dp = Dispatcher()
    await register_all_handlers(dp=dp)

    dp.startup.register(_run_global_task)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.info(f"{e}")
        await dp.stop_polling()
