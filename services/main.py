from pydantic import BaseModel
from database.methods.main import Database
from redis_.main import RedisClient
from .telegram_parser.main import TelegramParser


class ServiceData(BaseModel):
    state: dict
    type: str


class Service:

    def __init__(self, query: ServiceData):
        self.query = query
        self.db = Database()
        self.redis = RedisClient()

    async def init_job(self):

        if self.query.type == "telegram":
            ...
        elif self.query.type == "web":
            ...
        else:
            return "type not found"

    async def _get_telegram_parser_tool(self):
        telegram_pars_entity = TelegramParser()
