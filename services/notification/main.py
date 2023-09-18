from datetime import datetime

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, Chat, InputFile

from database.methods.main import Database
from settings.config import settings
from bot.keyboards.inline import approve_message


class Notification:
    data: list = []

    def __init__(self, type_: str, data: list):
        self.type_ = type_
        self.data = data
        self.database = Database()

    async def send_message(self, bot: Bot):

        if self.type_ == "approve_message":
            update_data = []
            for new_post in self.data:
                unit = {new_post.id: new_post.approve_state}
                update_data.append(unit)

                photo_data = await self.database.get_photo_by_cin_and_msg_id(channel_id=, message_id=new_post.post_id)
                photo = InputFile()
                await bot.send_photo(chat_id=settings.admin.id_, photo=photo, caption="⚠️ Новый пост на проверку: ⚠️\n\n"
                                            f"{new_post.text}", reply_markup=approve_message(new_post))
                # await bot.send_message(settings.admin.id_,
                #                        text="⚠️ Новый пост на проверку: ⚠️\n\n"
                #                             f"{new_post.text}", reply_markup=approve_message(new_post))

            for post in update_data:
                for k, v in post.items():
                    await self.database.update_mod_post(post_id=k, data={"approve_state": v})
        else:
            return 'error'
