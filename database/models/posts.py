from sqlalchemy import Column, BigInteger, String, Table, MetaData, Integer
from pydantic import BaseModel
from bot.database.main import Base

metadata = MetaData()


class PostData(BaseModel):
    channel_id: int
    message_id: int
    date: str
    text: str
    state: str
    views_count: int
    reactions_count: int = 0
    comments_channel_id: int = 0
    type: str = "Text"
    id: int = 0

    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "message_id": self.message_id,
            "date": self.date,
            "text": self.text,
            "state": self.state,
            "views_count": self.views_count,
            "reactions_count": self.reactions_count,
            "comments_channel_id": self.comments_channel_id,
            "type": self.type,
            "id": self.id
        }


class Post(Base):
    __table__ = Table(
        "post",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("channel_id", BigInteger, nullable=False),
        Column("message_id", BigInteger, nullable=False),
        Column("date", String, nullable=False),
        Column("type", String),
        Column("state", String, nullable=False),
        Column("text", String, nullable=False),
        Column("reactions_count", Integer),
        Column("views_count", Integer, nullable=False),
        Column("comments_channel_id", BigInteger, nullable=False)
    )

    def __init__(self, post: PostData):
        self.channel_id = post.channel_id
        self.message_id = post.message_id
        self.date = post.date
        self.type = post.type
        self.state = post.state
        self.text = post.text
        self.reactions_count = post.reactions_count
        self.views_count = post.views_count
        self.comments_channel_id = post.comments_channel_id
