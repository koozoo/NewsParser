import logging
from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from bot.keyboards.inline import admin_menu, user_menu
from settings.config import settings


async def cmd_start(message: Message):
    user_id = message.from_user.id

    if settings.admin.id_ == user_id:
        await message.answer(f"Привет admin -> твой id: {user_id}",
                             reply_markup=admin_menu())
    else:
        await message.answer(text=f"Привет user -> твой id: {user_id}",
                             reply_markup=user_menu())


async def register_commands_handler(dp: Dispatcher):
    logging.info("REGISTER ALL ADMIN HANDLERS")
    dp.message.register(cmd_start, Command(commands=['start']))
