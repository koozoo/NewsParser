import logging
from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from services.main import Service


async def cmd_start(message: Message):
    service_entity = Service()

    await service_entity.init_auth(context=message)


async def register_commands_handler(dp: Dispatcher):
    logging.info("REGISTER ALL COMMANDS HANDLERS")
    dp.message.register(cmd_start, Command(commands=['start']))
