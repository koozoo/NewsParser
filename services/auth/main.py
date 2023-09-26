from aiogram.types import Message

from bot.keyboards.inline import admin_menu, user_menu
from bot.view.main import View
from database.methods.main import Database
from database.models.user import UserData
from scheduler.main import scheduler
from services.cache.cache import Cache
from settings.config import settings


class Auth:

    def __init__(self, context: Message):
        self.user_id = context.from_user.id
        self.is_admin = False
        self.user: UserData
        self.database = Database()
        self.context = context
        self.view = View(context=context)
        self.cache = Cache()

    async def authorization(self):
        await self.context.delete()

        name = self.context.from_user.full_name
        messages = {"admin": f"Привет {name}.\n"
                             f"Права доступа: Администратор",
                    "user": f"Привет {name}.\n"
                            f"Права доступа: Пользователь"
                    }

        if await self._check_user():
            user = await self.database.get_user(user_id=self.user_id)

            if user.is_admin and user.id != 0:
                await self.view.delete_message(msg_id=user.active_msg_id)
                await self.view.print_message(text=messages['admin'], kb=admin_menu)
            elif user.id == settings.admin.id_:
                await self.view.delete_message(msg_id=user.active_msg_id)
                await self.view.print_message(text=messages['admin'], kb=admin_menu)
            else:
                await self.view.delete_message(msg_id=user.active_msg_id)
                await self.view.print_message(text=messages['user'], kb=user_menu)
        else:
            if self.user_id == settings.admin.id_:
                message_entity = await self.context.answer(text=messages['admin'],
                                                           reply_markup=admin_menu())
                user = UserData(id=self.user_id,
                                name=self.context.from_user.full_name,
                                active_msg_id=message_entity.message_id,
                                is_admin=True)

            else:
                message_entity = await self.context.answer(text=messages['user'],
                                                           reply_markup=user_menu())

                user = UserData(id=self.user_id,
                                active_msg_id=message_entity.message_id,
                                name=self.context.from_user.full_name)

            scheduler.add_job(self.database.add_user, kwargs={"user": user})

    async def _check_user(self):
        return await self.database.check_user(user_id=self.user_id)
