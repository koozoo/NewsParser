from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models.modify_post import ModifyPostData


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


def approve_message(new_post: ModifyPostData):

    bts = {
        "Опубликовать ✅": f"MESSAGE_approve_{new_post.id}:{new_post.post_id}:{new_post.channel_id}",
        "Преписать ♻️": f"MESSAGE_repeat_{new_post.id}:{new_post.post_id}:{new_post.channel_id}",
        "Отклонить 🚫": f"MESSAGE_reject_{new_post.id}:{new_post.post_id}:{new_post.channel_id}"
    }

    builder = InlineKeyboardBuilder()

    for btn_title, btn_callback in bts.items():
        b = InlineKeyboardButton(text=btn_title, callback_data=btn_callback)
        builder.add(b)

    return builder.as_markup()
