from aiogram import Bot
from aiogram.types import FSInputFile

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

                if new_post.type == "photo" or new_post.type == "wep_page":

                    photo_data = await self.database.get_photo_by_cin_and_msg_id(channel_id=new_post.channel_id,
                                                                                 message_id=new_post.post_id)
                    print("photo in notify 29 string", photo_data)
                    if photo_data:
                        photo = FSInputFile(path=photo_data['data'].photo_path)
                        await bot.send_photo(settings.admin.id_, photo=photo,
                                             caption="⚠️ Новый пост на проверку: ⚠️\n\n"
                                                     f"{new_post.text}",
                                             reply_markup=approve_message(new_post))

                else:
                    await bot.send_message(settings.admin.id_,
                                           text="⚠️ Новый пост на проверку: ⚠️\n\n"
                                                f"{new_post.text}",
                                           reply_markup=approve_message(new_post))

            for post in update_data:
                for k, v in post.items():
                    await self.database.update_mod_post(post_id=k, data={"approve_state": v})
        else:
            return 'error'
