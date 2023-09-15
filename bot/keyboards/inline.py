from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_menu():
    bts = {
        "Добавить канал": "ADMIN_add_chanel",
        "Обновить данные": "ADMIN_UPDATE_data",
        "Узнать id канала": "TOOL_GetChannelId",
        "Профиль": "PROFILE_admin"
    }

    builder = InlineKeyboardBuilder()

    for btn_title, btn_callback in bts.items():
        b = InlineKeyboardButton(text=btn_title, callback_data=btn_callback)
        builder.add(b)

    return builder.as_markup()


def user_menu():
    bts = {
        "Написать админу": "USER_send",
        "Профиль": "PROFILE_user"
    }

    builder = InlineKeyboardBuilder()

    for btn_title, btn_callback in bts.items():
        b = InlineKeyboardButton(text=btn_title, callback_data=btn_callback)
        builder.add(b)

    return builder.as_markup()


def user_profile_menu():
    bts = {
        "Мой id": "TOOL_GetMyId"
    }

    builder = InlineKeyboardBuilder()

    for btn_title, btn_callback in bts.items():
        b = InlineKeyboardButton(text=btn_title, callback_data=btn_callback)
        builder.add(b)

    return builder.as_markup()


def admin_profile_menu():
    bts = {
        "Мой id": "TOOL_GetMyId",
    }

    builder = InlineKeyboardBuilder()

    for btn_title, btn_callback in bts.items():
        b = InlineKeyboardButton(text=btn_title, callback_data=btn_callback)
        builder.add(b)

    return builder.as_markup()
