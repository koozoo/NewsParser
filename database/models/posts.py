import datetime as dt
from sqlalchemy import Column, BigInteger, String, Table, MetaData, Boolean
from pydantic import BaseModel
from database.main import Base

metadata = MetaData()


class PostData(BaseModel):
    channel_id: int = 0
    message_id: int = 0
    title: str = "none"
    date: str
    text: str
    state: str = "new"  # для обработки задач для openAI
    is_published: bool = False  # отправлять на публикацию
    modified_text: str = "none"
    type: str = "Text"
    id: int = 0
    is_old: bool = False
    url: str = "none"

    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "message_id": self.message_id,
            "title": self.title,
            "date": self.date,
            "text": self.text,
            "state": self.state,
            # new(создано системой но в работу еще не запущено), pending(ожидает обработки текста), process(текст в обработке), await(ожидает подтверждения), done, closed
            "type": self.type,
            "is_published": self.is_published,
            "modified_text": self.modified_text,
            "id": self.id,
            "is_old": self.is_old
        }

    @staticmethod
    def dict_to_post_data(data: dict):
        return PostData(channel_id=data.get('channel_id', 0),
                        message_id=data.get('message_id', 0),
                        title=data.get('title', "none"),
                        date=data.get('date', dt.datetime.utcnow()),
                        text=data.get('text', ""),
                        state=data.get('state', "new"),
                        type=data.get('type', "none"),
                        is_published=data.get('is_published', False),
                        modified_text=data.get('modified_text', "none"),
                        id=data.get('id', 0),
                        is_old=data.get('is_old', False),
                        url=data.get('url', "none"))


class Post(Base):
    __table__ = Table(
        "post",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("channel_id", BigInteger, nullable=False),
        Column("message_id", BigInteger, nullable=False),
        Column("title", String, nullable=False),
        Column("date", String, nullable=False),
        Column("type", String),
        Column("state", String, nullable=False),
        Column("text", String, nullable=False),
        Column("modified_text", String),
        Column("is_old", Boolean, default=False)
    )

    def __init__(self, post: PostData):
        self.channel_id = post.channel_id
        self.message_id = post.message_id
        self.title = post.title
        self.date = post.date
        self.type = post.type
        self.state = post.state
        self.text = post.text
        self.modified_text = post.modified_text
        self.is_old = post.is_old
