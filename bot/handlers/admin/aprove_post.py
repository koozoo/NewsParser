import os

from aiogram.types import CallbackQuery, FSInputFile

from database.models.media import MediaData
from scheduler.main import scheduler
from database.methods.main import Database
from services.cache.cache import Cache
from settings.config import settings


class PublishPost:

    def __init__(self, message_id: int, channel_id: int, context: CallbackQuery, type_: str):
        self.context = context
        self.message_id = message_id
        self.channel_id = channel_id
        self._database = Database()
        self._cache = Cache()
        self.type_ = type_

    async def _send_message(self, post):
        await self.context.bot.send_message(chat_id=f"-100{settings.project_const.channel_id}", text=post)

    async def _send_media(self, post, **media):
        photo = FSInputFile(path=media['media']['data'].photo_path)
        print(photo)
        await self.context.bot.send_photo(chat_id=f"-100{settings.project_const.channel_id}", photo=photo, caption=post)

    async def start(self, post, media=None):
        if self.type_ == "text":
            await self._send_message(post=post)
        else:
            await self._send_media(post=post, media=media)


class ApprovePost:

    def __init__(self, callback: str, context: CallbackQuery):
        self.callback = callback
        self.context = context
        self.database = Database()
        self.cache = Cache()

    async def _del_msg(self):
        try:
            await self.context.bot.delete_message(chat_id=settings.admin.id_,
                                                  message_id=self.context.message.message_id)
        except Exception as e:
            print(e)

    async def _approve(self, data):
        mod_post_id = int(data[0])
        message_id = int(data[1])
        channel_id = int(data[2])

        await self._del_msg()

        mod_text = await self.database.get_mod_post_by_id(post_id=mod_post_id)

        if mod_text:
            mod_text = mod_text[0]
        else:
            mod_text = "none"

        update_data_post = {
            "state": "close",
            "modified_text": mod_text,
            "published": True
        }

        update_data_mod_post = {
            "approve_state": "close"
        }

        post = await self.database.get_post_(message_id=message_id, channel_id=channel_id)

        scheduler.add_job(self.database.update_post, kwargs={
            "post_id": post[0].id, "data": update_data_post
        })
        scheduler.add_job(self.database.update_mod_post, kwargs={
            "post_id": mod_post_id, "data": update_data_mod_post
        })

        if post[0].type == "photo" or post[0].type == "web_page":
            media = await self.database.get_photo_by_cin_and_msg_id(channel_id=channel_id, message_id=message_id)
            publish = PublishPost(message_id=message_id, channel_id=channel_id, context=self.context, type_="media")
        else:
            media = "none"
            publish = PublishPost(message_id=message_id, channel_id=channel_id, context=self.context, type_="text")

        if mod_text is not None:
            scheduler.add_job(publish.start, kwargs={"post": mod_text, "media": media})
            if post[0].type == "photo" or post[0].type == "web_page":
                if media != 'none':
                    update_data = {
                        "file_name": "delete"
                    }

                    print("media in approve psot ", media)
                    await self.database.update_media(media_id=media['data'].id, data=update_data)

    async def _reject(self, data):
        mod_post_id = int(data[0])
        message_id = int(data[1])
        channel_id = int(data[2])

        await self._del_msg()

        update_data_post = {
            "state": "reject"
        }

        update_data_mod_post = {
            "approve_state": "reject"
        }

        post = await self.database.get_post_(message_id=message_id, channel_id=channel_id)

        scheduler.add_job(self.database.update_post, kwargs={
            "post_id": post[0].id, "data": update_data_post
        })
        scheduler.add_job(self.database.update_mod_post, kwargs={
            "post_id": mod_post_id, "data": update_data_mod_post
        })

        if post[0].type == "photo" or post[0].type == "web_page":
            media = await self.database.get_photo_by_cin_and_msg_id(channel_id=channel_id, message_id=message_id)

            update_data = {
                "file_name": "delete"
            }

            await self.database.update_media(media_id=media['data'].id, data=update_data)

    async def _repeat(self, data):
        mod_post_id = int(data[0])
        message_id = int(data[1])
        channel_id = int(data[2])

        await self._del_msg()

        update_data_post = {
            "state": "new"
        }

        update_data_mod_post = {
            "approve_state": "reject"
        }

        post = await self.database.get_post_(message_id=message_id, channel_id=channel_id)

        scheduler.add_job(self.database.update_post, kwargs={
            "post_id": post[0].id, "data": update_data_post
        })
        scheduler.add_job(self.database.update_mod_post, kwargs={
            "post_id": mod_post_id, "data": update_data_mod_post
        })

    async def delete_photo(self, path: str):
        os.remove(path=path)

    async def type_router(self):
        callback_data = self.callback.split("_")
        print("CALLBACK FOR APPROVE POST ", callback_data)
        data_for_event = callback_data[2].split(":")

        match callback_data[1]:
            case "approve":
                await self._approve(data_for_event)
            case "reject":
                await self._reject(data_for_event)
            case "repeat":
                await self._repeat(data_for_event)
            case "_":
                "error"
