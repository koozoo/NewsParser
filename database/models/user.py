import datetime

from sqlalchemy import Column, BigInteger, String, Integer, Boolean, \
    Table, MetaData, TIMESTAMP
from pydantic import BaseModel
from bot.database.main import Base


class UserData(BaseModel):
    id: int
    full_name: str = "null"
    user_name: str = "null"
    role: int = 1
    phone: str = "null"
    email: str = "null"
    is_subscribed: bool = False


metadata = MetaData()


class User(Base):
    __table__ = Table(
        "user",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("role", Integer, nullable=False),
        Column("phone", String, nullable=False),
        Column("email", String, nullable=False),
        Column("full_name", String, nullable=False),
        Column("user_name", String, nullable=False),
        Column("is_subscribed", Boolean, nullable=False),
        Column("create_at", TIMESTAMP, default=datetime.datetime.utcnow(),
               nullable=False),
        Column("update_at", TIMESTAMP, default=datetime.datetime.utcnow(),
               nullable=False)
    )

    def __init__(self, user: UserData):
        self.id = user.id
        self.role = user.role
        self.full_name = user.full_name
        self.phone = user.phone
        self.email = user.email
        self.user_name = user.user_name
        self.is_subscribed = user.is_subscribed
