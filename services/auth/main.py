from aiogram.types import Message

from bot.keyboards.inline import admin_menu, user_menu
from database.methods.main import Database
from database.models.user import UserData
from scheduler.main import scheduler
from settings.config import settings


class Auth:

    def __init__(self, context: Message):
        self.user_id = context.from_user.id
        self.is_admin = False
        self.user: UserData
        self.database = Database()
        self.context = context

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
                await self.context.answer(text=messages['admin'],
                                          reply_markup=admin_menu())
            elif user.id == settings.admin.id_:
                await self.context.answer(text=messages['admin'],
                                          reply_markup=admin_menu())
            else:
                await self.context.answer(text=messages['user'],
                                          reply_markup=user_menu())
        else:
            if self.user_id == settings.admin.id_:
                user = UserData(id=self.user_id,
                                name=self.context.from_user.full_name,
                                is_admin=True)
                await self.context.answer(text=messages['admin'],
                                          reply_markup=admin_menu())
            else:
                user = UserData(id=self.user_id,
                                name=self.context.from_user.full_name)
                await self.context.answer(text=messages['user'],
                                          reply_markup=user_menu())

            scheduler.add_job(self.database.add_user, kwargs={"user": user})

    async def _check_user(self):
        return await self.database.check_user(user_id=self.user_id)
