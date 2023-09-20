from sqlalchemy import Column, BigInteger, String, Table, MetaData
from pydantic import BaseModel
from database.main import Base

metadata = MetaData()


class ModifyPostData(BaseModel):
    id: int = 0
    post_id: int
    text: str
    channel_id: int
    type: str
    approve_state: str = 'new'# new / await / approve / reject / close

    def to_dict(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "text": self.text,
            "channel_id": self.channel_id,
            "approve_state": self.approve_state,
            "type": self.type
        }


class ModifyPost(Base):
    __table__ = Table(
        "modify_post",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("post_id", BigInteger, nullable=False),
        Column("text", String, nullable=False),
        Column("channel_id", BigInteger),
        Column("approve_state", String, nullable=False),
        Column("type", String)
    )

    def __init__(self, post: ModifyPostData):
        self.post_id = post.post_id
        self.text = post.text
        self.channel_id = post.channel_id
        self.type = post.type
        self.approve_state = post.approve_state
