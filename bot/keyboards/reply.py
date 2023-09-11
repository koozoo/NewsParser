from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def yes_no():

    builder = ReplyKeyboardBuilder()

    builder.row(KeyboardButton(text="Да"), KeyboardButton(text="Нет"))
    return builder.as_markup(resize_keyboard=True)
