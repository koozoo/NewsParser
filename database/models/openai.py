from sqlalchemy import Column, BigInteger, String, \
    Table, MetaData
from pydantic import BaseModel
from database.main import Base


class OpenaiData(BaseModel):
    id: int = 0
    prompt: str = "null"
    type: str = "Default"

    def to_dict(self):
        return {
            "id": self.id,
            "prompt": self.prompt,
            "type": self.type
        }

    @staticmethod
    def dict_to_user_data(data: dict):
        return OpenaiData(id=data.get("id", 0),
                          name=data.get("prompt", "Noname"),
                          phone=data.get("type", "Default"))


metadata = MetaData()


class Openai(Base):
    __table__ = Table(
        "openai",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("prompt", String, nullable=False),
        Column("type", String, nullable=False)
    )

    def __init__(self, openai: OpenaiData):
        self.prompt = openai.prompt
        self.type = openai.type
