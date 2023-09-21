from aiogram.types import CallbackQuery
from scheduler.main import scheduler
from database.methods.main import Database
from services.cache.cache import Cache
from settings.config import settings


class PublishPost:

    def __init__(self, message_id: int, channel_id: int, context: CallbackQuery):
        self.context = context
        self.message_id = message_id
        self.channel_id = channel_id
        self._database = Database()
        self._cache = Cache()

    async def _send_message(self, post):
        await self.context.bot.send_message(chat_id=f"-100{settings.project_const.channel_id}", text=post)

    async def start(self, post):
        await self._send_message(post=post)


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

        publish = PublishPost(message_id=message_id, channel_id=channel_id, context=self.context)
        if mod_text is not None:
            scheduler.add_job(publish.start, kwargs={"post": mod_text})

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

    async def type_router(self):
        callback_data = self.callback.split("_")
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
