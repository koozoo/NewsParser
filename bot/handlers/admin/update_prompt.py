from database.methods.main import Database
from aiogram.types import CallbackQuery


class Prompt:

    def __init__(self, context: CallbackQuery):
        self._database = Database()
        self._context = context

    async def update_prompt(self):
        ...

    async def init_prompt(self):
        data = self._context.data.split("_")
        print(data)
