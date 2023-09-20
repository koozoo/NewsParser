import datetime as dt
from sqlalchemy import Column, BigInteger, String, Table, MetaData, Boolean
from pydantic import BaseModel
from database.main import Base

metadata = MetaData()


class PostData(BaseModel):
    channel_id: int = 0
    message_id: int = 0
    title: str = "none"
    date: str = dt.datetime.utcnow()
    text: str
    state: str = "new"  # для обработки задач для openAI
    modified_text: str = "none"
    type: str = "text"
    id: int = 0
    url: str = "none" # для web parsing
    published: bool = False # меняется после публикации
    reject: bool = False # удалить из подбоки статью
    media: dict = None

    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "message_id": self.message_id,
            "title": self.title,
            "date": self.date,
            "text": self.text,
            "state": self.state,
            # new(создано системой но в работу еще не запущено), pending(отправка в очередь для обработки текста), process(текст в обработке), await(ожидает подтверждения), done, closed
            "type": self.type,
            "modified_text": self.modified_text,
            "id": self.id,
            "published": self.published,
            "reject": self.reject,
            "media": self.media
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
                        modified_text=data.get('modified_text', "none"),
                        id=data.get('id', 0),
                        url=data.get('url', "none"),
                        published=data.get('published', False),
                        reject=data.get('reject', False),
                        media=data.get('media', {}))


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
        Column("published", Boolean, default=False),
        Column("reject", Boolean, default=False)
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
        self.published = post.published
        self.reject = post.reject
