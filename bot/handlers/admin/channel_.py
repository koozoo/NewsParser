from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.keyboards.inline import admin_menu, channel_menu, close, channel_back_to_admin_menu
from bot.keyboards.reply import yes_no
from bot.view.main import View
from services.telegram_parser.main import TelegramParser
from database.methods.main import Database
from aiogram.types import CallbackQuery, Message


class GetChannelAction(StatesGroup):
    link = State()
    finish = State()


class InterfaceGetChannel:

    @staticmethod
    async def text_for_get_channel(query: str, **data) -> str | None:
        texts = {
            "init": "Введите пожалуйста телеграмм адрес интересующего канала.\n\n"
                    "Пример: https://t.me/some_channel",
            "link_process": "Проверьте введенную ссылку, если верно нажмите Да, Нет чтобы ввести новую ссылку.",
            "filed_link_process": "Вы ввели некоректную ссылку.\n\n"
                                  "В ссылке должно быть https://t.me\n\n"
                                  "Попробуйте еще раз или нажмите меню, чтобы выйти.",
            "finish_process": f"ID: {data.get('id', 'link not found')}"
        }

        return texts.get(query, None)

    @staticmethod
    async def init_get_channel(call: CallbackQuery, state: FSMContext):
        view = View(context=call)
        await state.set_state(GetChannelAction.link)

        text = await InterfaceGetChannel.text_for_get_channel(query="init")

        if text is not None:
            await view.print_message(text=text, kb=channel_back_to_admin_menu)
        else:
            await view.print_message(text="Ошибка в тексте, пожалуйста начните заного.", kb=channel_back_to_admin_menu)

    @staticmethod
    async def link_process(message: Message, state: FSMContext):
        view = View(message)
        data = await state.get_data()
        await state.update_data(link=message.text)
        await state.set_state(GetChannelAction.finish)

        await view.delete_message()
        await view.delete_message(msg_id=data.get('msg_id', None))

        text = await InterfaceGetChannel.text_for_get_channel(query="link_process")
        message_entity = await message.answer(text=text, reply_markup=yes_no())

        await state.update_data(msg_id=message_entity.message_id)

    @staticmethod
    async def filed_link_process(message: Message, state: FSMContext):
        message_entity = await message.answer(
            text=await InterfaceGetChannel.text_for_get_channel(query="filed_link_process"))
        await state.update_data(msg_id=message_entity.message_id)

    @staticmethod
    async def finish_process(message: Message, state: FSMContext):
        await state.update_data(answer=message.text.casefold())
        data = await state.get_data()
        view = View(message)
        telegram_parser = TelegramParser()

        await view.delete_message()
        await view.delete_message(data['msg_id'])

        if data['answer'] == "да":
            id_ = await telegram_parser.get_full_channel_info(data['link'])
            id_ = id_.to_dict()
            text = await InterfaceGetChannel.text_for_get_channel(query="finish_process", id=id_['full_chat']['id'])

            await view.print_message(text=text, kb=admin_menu)

            await state.clear()
        else:
            await state.set_state(GetChannelAction.link)
            text = await InterfaceGetChannel.text_for_get_channel("init")
            await view.print_message(text=text, kb=channel_back_to_admin_menu)


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

    async def _route(self, link: list[str], state: FSMContext | None) -> dict:
        result_data = {}
        if len(link) > 2 and not link[1].isdigit():
            if link[1] != 'back' and link[1] != 'add':
                link_data = link[1].split(":")

                match link_data[1]:
                    case "all":
                        text, kb = await self._all()
                        await self.context.message.answer(text=text, reply_markup=kb())
                    case "id":
                        if state is not None:
                            await InterfaceGetChannel.init_get_channel(call=self.context, state=state)
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

    async def start(self, state: FSMContext | None):
        callback_data = self.context.data.split("_")

        view_data = await self._route(link=callback_data, state=state)

        if view_data:
            text = view_data.get('text', f"Привет {self.context.from_user.full_name}.\n"
                                 + f"Права доступа: Администратор")
            kb = view_data.get('kb', admin_menu)

            await self.view.print_message(text=text, kb=kb)
