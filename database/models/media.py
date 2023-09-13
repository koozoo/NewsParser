from sqlalchemy import Column, BigInteger, String, Integer, Table, MetaData
from pydantic import BaseModel
from database.main import Base

metadata = MetaData()


class MediaData(BaseModel):
    type: str
    id: int = 0
    post_id: int = 0
    file_name: str = "none"
    telegram_document_id: int = 0
    access_hash: int = 0
    file_reference: int = 0
    size: int = 0
    mime_type: str = "none"
    duration: float = 0
    url: str = 'none'
    web_id: str = 0


class Media(Base):
    __table__ = Table(
        "media",
        metadata,
        Column("id", BigInteger, primary_key=True),
    )

    def __init__(self, channel: MediaData):
        self.name = channel.name
        self.link = channel.link
        self.description = channel.description
        self.user_count = channel.user_count
        self.telegram_channel_id = channel.telegram_channel_id
