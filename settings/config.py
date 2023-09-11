import os

from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()


class DatabaseData(BaseModel):
    name: str
    host: str
    port: str
    pass_: str
    login: str

    def to_dict(self):
        return {
            "name": self.name,
            "host": self.host,
            "port": self.port,
            "pass_": self.pass_,
            "login": self.login
        }


class RedisData(BaseModel):
    host: str
    port: str
    pass_: str = None
    login: str = None

    def to_dict(self):
        return {
            "host": self.host,
            "port": self.port,
            "pass_": self.pass_,
            "login": self.login
        }


class AdminData(BaseModel):
    id_: int
    email: str

    def to_dict(self):
        return {
            "id": self.host,
            "email": self.port
        }


class BotData(BaseModel):
    token: str

    def to_dict(self):
        return {
            "token": self.token
        }


class TelegramParserData(BaseModel):
    api_hash: str
    api_id: str
    max_update_post: int

    def to_dict(self):
        return {
            "api_hash,": self.api_hash,
            "api_id": self.api_id,
            "max_update_post": self.max_update_post
        }


class OpenAiData(BaseModel):
    open_ai_token: str
    open_ai_organization: str

    def to_dict(self):
        return {
            "open_ai_token,": self.open_ai_token,
            "open_ai_organization": self.open_ai_organization
        }


class SettingsData(BaseModel):
    redis: RedisData
    database_: DatabaseData
    bot: BotData
    telegram_parser: TelegramParserData
    web_parser: dict
    open_ai: OpenAiData
    admin: AdminData


class Settings:

    settings: None

    def _get_config_db(self):
        db_name = os.getenv("DB_NAME")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_pass = os.getenv("DB_PASS")
        db_login = os.getenv("DB_LOGIN")

        return DatabaseData(name=db_name, host=db_host, port=db_port, pass_=db_pass, login=db_login)

    def _get_config_redis(self):
        redis_host = os.getenv("REDIS_HOST")
        redis_port = os.getenv("REDIS_PORT")

        return RedisData(host=redis_host, port=redis_port)

    def _get_config_ui_bot_token(self):
        token = os.getenv("UiBotToken")

        return BotData(token=token)

    def _get_config_parser_bot_token(self):
        api_hash = os.getenv("ParserBotApiHash")
        api_id = os.getenv("ParserBotApiId")
        max_update_post = 50

        return TelegramParserData(api_hash=api_hash, api_id=api_id, max_update_post=max_update_post)

    def _get_config_open_ai_token(self):
        open_ai_token = os.getenv("OPEN_AI_TOKEN")
        open_ai_organization = os.getenv("OPEN_AI_ORGANIZATION")

        return OpenAiData(open_ai_token=open_ai_token, open_ai_organization=open_ai_organization)

    def _get_config_web_parser(self) -> dict:
        return {}

    def _get_admin(self) -> AdminData:
        admin_id = os.getenv("ADMIN_ID")
        admin_email = os.getenv("ADMIN_EMAIL")
        return AdminData(id_=admin_id, email=admin_email)

    def get_settings(self) -> SettingsData:
        return SettingsData(database_=self._get_config_db(),
                            redis=self._get_config_redis(),
                            bot=self._get_config_ui_bot_token(),
                            telegram_parser=self._get_config_parser_bot_token(),
                            web_parser=self._get_config_web_parser(),
                            open_ai=self._get_config_open_ai_token(),
                            admin=self._get_admin())


settings = Settings().get_settings()
