import logging
from aiogram import Dispatcher, F
from aiogram.types import CallbackQuery


async def add_channel(call: CallbackQuery):
    uid = call.from_user.id
    await call.message.answer(text=f"ID: {uid}, callback: {call.data}")


async def register_admin_handlers(dp: Dispatcher):
    logging.info("REGISTER ALL ADMIN HANDLERS")
    dp.callback_query.register(add_channel, F.data.startswith("ADMIN"))
