import datetime as dt

from sqlalchemy import Column, BigInteger, String, Boolean, \
    Table, MetaData, TIMESTAMP, Integer
from pydantic import BaseModel
from database.main import Base


class UserData(BaseModel):
    id: int
    name: str = "null"
    phone: str = "null"
    email: str = "null"
    active_msg_id: int = 0
    is_admin: bool = False
    update_at: dt.datetime = dt.datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "active_msg_id": self.active_msg_id,
            "is_admin": self.is_admin,
            "update_at": self.update_at
        }

    @staticmethod
    def dict_to_user_data(data: dict):

        return UserData(id=data.get("id", 0),
                        name=data.get("name", "Noname"),
                        phone=data.get("phone", "none"),
                        email=data.get("email", "none"),
                        active_msg_id=data.get("active_msg_id", 0),
                        is_admin=data.get("is_admin", False),
                        update_at=data.get("update_at", dt.datetime.utcnow()))


metadata = MetaData()


class User(Base):
    __table__ = Table(
        "user",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("phone", String, nullable=False),
        Column("email", String, nullable=False),
        Column("name", String, nullable=False),
        Column("is_admin", Boolean, nullable=False),
        Column("active_msg_id", Integer, nullable=False),
        Column("create_at", TIMESTAMP, default=dt.datetime.utcnow(),
               nullable=False),
        Column("update_at", TIMESTAMP, default=dt.datetime.utcnow(),
               nullable=False)
    )

    def __init__(self, user: UserData):
        self.id = user.id
        self.name = user.name
        self.phone = user.phone
        self.email = user.email
        self.is_admin = user.is_admin
        self.active_msg_id = user.active_msg_id
