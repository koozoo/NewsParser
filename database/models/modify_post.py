from sqlalchemy import Column, BigInteger, String, Table, MetaData
from pydantic import BaseModel
from database.main import Base

metadata = MetaData()


class PostData(BaseModel):
    id: int
    post_id: int
    text: str
    approve_state: str # new / approve / reject

    def to_dict(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "text": self.text,
            "approve_state": self.approve_state
        }


class Post(Base):
    __table__ = Table(
        "modify_post",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("post_id", BigInteger, nullable=False),
        Column("text", String, nullable=False),
        Column("approve_state", String, nullable=False)
    )

    def __init__(self, post: PostData):
        self.post_id = post.post_id
        self.text = post.text
        self.approve_state = post.approve_state
