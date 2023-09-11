from sqlalchemy import Column, BigInteger, String, Table, MetaData, Boolean
from pydantic import BaseModel
from database.main import Base

metadata = MetaData()


class PostData(BaseModel):
    channel_id: int
    message_id: int
    title: str
    date: str
    text: str
    state: str # для обработки задач для openAI
    is_published: bool # отправлять на публикацию
    modified_text: str
    type: str = "Text"
    id: int = 0

    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "message_id": self.message_id,
            "title": self.title,
            "date": self.date,
            "text": self.text,
            "state": self.state, # create(ожидает обработки текста), process(текст в обработке), await(ожидает подтверждения), done, closed
            "type": self.type,
            "is_published": self.is_published,
            "modified_text": self.modified_text,
            "id": self.id
        }


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
        Column("modified_text", String)
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
