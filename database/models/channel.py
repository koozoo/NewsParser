from sqlalchemy import Column, BigInteger, String, Integer, Table, MetaData
from pydantic import BaseModel
from database.main import Base

metadata = MetaData()


class ChannelData(BaseModel):
    link: str
    id: int = 0
    name: str = "none"
    description: str = "none"
    user_count: int = 0
    telegram_channel_id: int = 0

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "link": self.link,
            "description": self.description,
            "user_count": self.user_count,
            "telegram_channel_id": self.telegram_channel_id
        }

    @staticmethod
    def dict_to_channel_data(data: dict):
        return ChannelData(id=data.get('id', 0),
                           name=data.get('name', 'Noname'),
                           link=data.get('link', 'none'),
                           description=data.get('description', 'none'),
                           user_count=data.get('user_count', 0),
                           telegram_channel_id=data.get("telegram_channel_id", 0))


class Channel(Base):
    __table__ = Table(
        "channel",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("telegram_channel_id", BigInteger),
        Column("name", String, nullable=False),
        Column("link", String, nullable=False),
        Column("description", String, nullable=False),
        Column("user_count", Integer, nullable=False)
    )

    def __init__(self, channel: ChannelData):
        self.name = channel.name
        self.link = channel.link
        self.description = channel.description
        self.user_count = channel.user_count
        self.telegram_channel_id = channel.telegram_channel_id
