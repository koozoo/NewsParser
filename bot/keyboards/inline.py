from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models.modify_post import ModifyPostData


def admin_menu():
    builder = InlineKeyboardBuilder()

    b_add = InlineKeyboardButton(text="🖍 Добавить канал", callback_data="ADMIN_add_chanel")
    b_right = InlineKeyboardButton(text="🔐 Права доступа", callback_data="ADMIN_rights")
    b_channel_id = InlineKeyboardButton(text="🔢 Узнать id канала", callback_data="TOOL_GetChannelId")
    b_profile = InlineKeyboardButton(text="📋 Профиль", callback_data="PROFILE_admin")

    builder.row(b_add).row(b_right, b_channel_id).row(b_profile)

    return builder.as_markup()


def admin_rights_menu():
    bts = {
        "Добавить админа": "ADMIN_rights_add",
        "Удалить админа": "ADMIN_rights_delete",
        "Удалить всех админов": "ADMIN_rights_delete:all",
        "Назад": "ADMIN_menu"
    }

    builder = InlineKeyboardBuilder()

    b_add = InlineKeyboardButton(text="Добавить админа", callback_data="ADMIN_rights_add")
    b_delete = InlineKeyboardButton(text="Удалить админа", callback_data="ADMIN_rights_delete")
    delete_all = InlineKeyboardButton(text="Удалить всех админов", callback_data="ADMIN_rights_delete:all")
    b_back = InlineKeyboardButton(text="Назад", callback_data="ADMIN_menu")

    builder.row(b_add).row(b_delete, delete_all).row(b_back)

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
