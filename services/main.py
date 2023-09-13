from aiogram.types import Message
from database.methods.main import Database
from redis_.main import RedisClient
from .telegram_parser.main import TelegramParser
from .auth.main import Auth
from .web_parser.main import WebParser


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
