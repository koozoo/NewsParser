from aiogram.types import CallbackQuery

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

    async def _prepare_message(self):
        post = await self._database.get_post_for_publish(message_id=self.message_id, channel_id=self.channel_id)
        if post:
            await self._send_message(post=post[0].modified_text)

    async def start(self):
        await self._prepare_message()
