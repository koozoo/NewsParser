from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from database.models.modify_post import ModifyPostData


def admin_menu(msg_id: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    b_right = InlineKeyboardButton(text="🔐 Права доступа", callback_data=f"ADMIN_rights_{msg_id}")
    b_prompt = InlineKeyboardButton(text="🔁 Обновить prompt", callback_data=f"PROMPT_update_{msg_id}")
    b_profile = InlineKeyboardButton(text="📋 Профиль", callback_data=f"PROFILE_admin_{msg_id}")
    b_channel_ = InlineKeyboardButton(text="🎛 Управление каналом", callback_data=f"CHANNEL_{msg_id}")

    builder.row(b_right).row(b_prompt).row(b_channel_).row(b_profile)

    return builder.as_markup()


def channel_back_to_admin_menu(msg_id: int):
    builder = InlineKeyboardBuilder()

    b_back_to_main_admin_menu = InlineKeyboardButton(text="⬅️ Меню", callback_data=f"CHANNEL_back_{msg_id}")

    builder.row(b_back_to_main_admin_menu)

    return builder.as_markup()


def channel_menu(msg_id: int):
    builder = InlineKeyboardBuilder()

    b_add = InlineKeyboardButton(text="🖍 Добавить канал", callback_data=f"ADMIN_add_chanel_{msg_id}")
    b_channel_id = InlineKeyboardButton(text="🔢 Узнать id канала", callback_data=f"CHANNEL_get:id_{msg_id}")
    b_channel_all = InlineKeyboardButton(text="📜 Все каналы", callback_data=f"CHANNEL_get:all_{msg_id}")
    b_delete_channel = InlineKeyboardButton(text="❌ Удалить канал", callback_data=f"ADMIN_delete_{msg_id}")
    b_back = InlineKeyboardButton(text="↩️ Назад", callback_data=f"CHANNEL_back_{msg_id}")

    builder.row(b_add).row(b_delete_channel).row(b_channel_all).row(b_channel_id).row(b_back)

    return builder.as_markup()


def admin_rights_menu(msg_id: int):
    bts = {
        "Добавить админа": f"ADMIN_rights_add_{msg_id}",
        "Удалить админа": f"ADMIN_rights_delete_{msg_id}",
        "Удалить всех админов": f"ADMIN_rights_delete:all_{msg_id}",
        "⬅️ Меню": f"CHANNEL_back_{msg_id}"
    }

    builder = InlineKeyboardBuilder()

    b_add = InlineKeyboardButton(text="Добавить админа", callback_data=f"ADMIN_rights_add_{msg_id}")
    b_delete = InlineKeyboardButton(text="Удалить админа", callback_data=f"ADMIN_rights_delete_{msg_id}")
    delete_all = InlineKeyboardButton(text="Удалить всех админов", callback_data=f"ADMIN_rights_delete:all_{msg_id}")
    b_back = InlineKeyboardButton(text="⬅️ Меню", callback_data=f"CHANNEL_back_{msg_id}")

    builder.row(b_add).row(b_delete, delete_all).row(b_back)

    return builder.as_markup()
    

def user_menu(msg_id: int = 0):
    bts = {
        "Написать админу": f"USER_send_{msg_id}",
        "Профиfль": f"PROFILE_user_{msg_id}"
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
