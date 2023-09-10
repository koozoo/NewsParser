from sqlalchemy import Column, BigInteger, String, Table, MetaData, Integer, Boolian
from pydantic import BaseModel
from database.main import Base

metadata = MetaData()


class PostData(BaseModel):
    channel_id: int
    message_id: int
    title: str
    date: str
    text: str
    state: str
    type: str = "Text"
    id: int = 0
    is_published: bool
    modified_text: str
    for_checking: bool


    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "message_id": self.message_id,
            "title": self.title,
            "date": self.date,
            "text": self.text,
            "state": self.state, # await(ожидает обработки текста), process(текст в обработке), done(modified_text готов)
            "type": self.type,
            "is_published": self.is_published,
            "modified_text": self.modified_text,
            "id": self.id,
            "for_checking": self.for_checking # "отправить на проверку"
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
        Column("modified_text", String),
        Column("for_checking", Boolian, nullable=False),
    )

    def __init__(self, post: PostData):
        self.channel_id = post.channel_id
        self.message_id = post.message_id
        self.title = post.title
        self.date = post.date
        self.type = post.type
        self.state = post.state
        self.text = post.text
