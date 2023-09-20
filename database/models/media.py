from sqlalchemy import Column, BigInteger, String, Table, MetaData
from pydantic import BaseModel
from database.main import Base
from database.models.posts import PostData

metadata = MetaData()


class MediaData(BaseModel):
    type: str
    id: int = 0
    post_id: int = 0
    file_name: str = "none"
    telegram_document_id: int = 0
    access_hash: int = 0
    file_reference: str = 'none'
    url: str = 'none'
    web_id: int = 0
    channel_id: int = 0

    def to_dict(self):
        return {
            "type": self.type,
            "id": self.id,
            "post_id": self.post_id,
            "file_name": self.file_name,
            "telegram_document_id": self.telegram_document_id,
            "access_hash": self.access_hash,
            "file_reference": self.file_reference,
            "url": self.url,
            "web_id": self.web_id,
            "channel_id": self.channel_id
        }

    @staticmethod
    def post_data_to_media_data(data: PostData):
        return MediaData(type=data.media['type'],
                         post_id=data.media['post_id'],
                         url=data.media['url'],
                         web_id=data.media['web_id'],
                         telegram_document_id=data.media['telegram_document_id'],
                         access_hash=data.media['access_hash'],
                         file_reference=data.media['file_reference'],
                         channel_id=data.media['channel_id'])


class Media(Base):
    __table__ = Table(
        "media",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("type", String),
        Column("post_id", BigInteger),
        Column("file_name", String),
        Column("telegram_document_id", BigInteger),
        Column("access_hash", BigInteger),
        Column("file_reference", String),
        Column("url", String),
        Column("web_id", BigInteger),
        Column("channel_id", BigInteger)
    )

    def __init__(self, channel: MediaData):
        self.type = channel.type
        self.post_id = channel.post_id
        self.file_name = channel.file_name
        self.telegram_document_id = channel.telegram_document_id
        self.access_hash = channel.access_hash
        self.file_reference = channel.file_reference
        self.url = channel.url
        self.web_id = channel.web_id
        self.channel_id = channel.channel_id
