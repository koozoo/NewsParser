import datetime

from sqlalchemy import Column, BigInteger, String, Table, MetaData, TIMESTAMP
from pydantic import BaseModel
from bot.database.main import Base

metadata = MetaData()


class TaskData(BaseModel):
    type: str
    user_id: int
    urls: str
    id: int = 0
    status: str = "create"
    create_at: datetime.datetime = datetime.datetime.utcnow()


class Task(Base):
    __table__ = Table(
        "msg_broker",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("type", String, nullable=False),
        Column("user_id", BigInteger, nullable=False),
        Column("status", String, nullable=False),
        Column("urls", String, nullable=False),
        Column("create_at", TIMESTAMP, nullable=False)
    )

    def __init__(self, task: TaskData):
        self.type = task.type
        self.user_id = task.user_id
        self.status = task.status
        self.create_at = task.create_at
        self.urls = task.urls
        if task.id != 0:
            self.id = task.id
