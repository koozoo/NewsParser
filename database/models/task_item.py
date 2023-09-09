import datetime

from sqlalchemy import Column, BigInteger, String, Table, MetaData, TIMESTAMP
from pydantic import BaseModel
from bot.database.main import Base

metadata = MetaData()


class TaskItemData(BaseModel):
    task_id: int
    target_url: str
    channel_id: int
    id: int = None
    status: str = "create"

    def to_dict(self):
        return {"task_id": self.task_id,
                "target_url": self.target_url,
                "channel_id": self.channel_id,
                "id": self.id,
                "status": self.status}

    def dict_to_obj(self, item: dict):
        return TaskItemData(task_id=item['task_id'],
                            target_url=item['target_url'],
                            channel_id=item['channel_id'],
                            id=item['id'],
                            status=item['status'])


class TaskItem(Base):
    __table__ = Table(
        "taskitem",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("task_id", BigInteger, nullable=False),
        Column("channel_id", BigInteger, nullable=False),
        Column("target_url", String, nullable=False),
        Column("status", String, nullable=False),
        Column("create_at", TIMESTAMP, default=datetime.datetime.utcnow(),
               nullable=False),
        Column("finished_at", TIMESTAMP, default=datetime.datetime.utcnow(),
               nullable=False)
    )

    def __init__(self, task_item: TaskItemData):
        self.task_id = task_item.task_id
        self.channel_id = task_item.channel_id
        self.target_url = task_item.target_url
        self.status = task_item.status
        if task_item.id != 0:
            self.id = task_item.id
