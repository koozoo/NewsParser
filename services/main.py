from aiogram import Bot
from aiogram.types import Message
from database.methods.main import Database
from redis_.main import RedisClient
from .notification.main import Notification
from .telegram_parser.main import TelegramParser
from .auth.main import Auth
from .web_parser.main import WebParser
from worker.tasks import add_openai_job


class Service:

    def __init__(self):
        self.db = Database()
        self.redis = RedisClient()

    async def init_parsing(self, type_: str):

        if type_ == "telegram":
            tool_entity = await self._start_telegram_parser()
        elif type_ == "web":
            ...
        else:
            return "type not found"

    async def _start_telegram_parser(self):
        telegram_pars_entity = TelegramParser()
        await telegram_pars_entity.start_parsing()

    async def _start_web_parsing(self):
        web_pars_entity = WebParser()

    async def init_auth(self, context: Message):
        auth = Auth(context=context)
        await auth.authorization()

    async def init_open_ai(self):
        await self._task_openai()

    async def _task_openai(self):
        add_openai_job.delay()

    async def init_approve_notification(self, bot: Bot):
        posts_for_notification = await self.db.get_posts_for_approve()

        notification = Notification(type_='approve_message', data=posts_for_notification["posts"])
        await notification.send_message(bot=bot)
