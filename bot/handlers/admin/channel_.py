from aiogram.fsm.context import FSMContext

from bot.handlers.admin.delete_channel import InterfaceFsmDelete, DeleteAction
from bot.keyboards.inline import admin_menu, channel_back_to_admin_menu, channel_menu, close
from bot.view.main import View
from services.telegram_parser.main import TelegramParser
from database.methods.main import Database
from aiogram.types import CallbackQuery


class ChannelMenu:

    def __init__(self, context: CallbackQuery):
        self._database = Database()
        self.context = context
        self.view = View(context=context)

    async def _all(self):
        text = await self._get_text_all_channel()
        kb = close
        return text, kb

    async def _back(self):
        text = f"Привет {self.context.from_user.full_name}.\n" \
               f"Права доступа: Администратор"
        kb = admin_menu

        return text, kb

    async def _main_chanel_menu(self):
        text = ("Права доступа: Администратор\n\n"
                "В данном разделе вы можете узнать:\n"
                "1. Добавить новый канал.\n"
                "2. Посмотреть все добавленные каналы.\n"
                "3. Удаление канала.\n"
                "4. Узнать ID любого канала, для дальнейшего добавления в парсер.")

        kb = channel_menu

        return text, kb

    async def _get_any_channel_id(self, link: str):
        parser_entity = TelegramParser()
        return await parser_entity.get_full_channel_info(link=link)

    async def _route(self, link: list[str]) -> dict:
        result_data = {}
        if len(link) > 2 and not link[1].isdigit():
            if link[1] != 'back' and link[1] != 'add':
                link_data = link[1].split(":")

                match link_data[1]:
                    case "all":
                        # result_data['text'], result_data['kb'] = await self._all()
                        text, kb = await self._all()
                        await self.context.message.answer(text=text, reply_markup=kb())
                    case "id":
                        ...
            elif link[1] == 'back':
                result_data['text'], result_data['kb'] = await self._back()
        else:
            result_data['text'], result_data['kb'] = await self._main_chanel_menu()

        return result_data

    async def _get_text_all_channel(self):
        result = ''
        for channel in await self._database.get_channels():
            result += f"ID: {channel.id} | LINK: {channel.link}\n"
        return result

    async def start(self):
        callback_data = self.context.data.split("_")

        view_data = await self._route(link=callback_data)

        if view_data:
            text = view_data.get('text', f"Привет {self.context.from_user.full_name}.\n"
                                 + f"Права доступа: Администратор")
            kb = view_data.get('kb', admin_menu)

            await self.view.print_message(text=text, kb=kb)

