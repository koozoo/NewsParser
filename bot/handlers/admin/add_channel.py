from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from bot.keyboards.inline import admin_menu
from bot.keyboards.reply import yes_no
from bot.handlers.utils import is_email
from bot.view.main import View
from database.methods.main import Database
from database.models.channel import ChannelData
from scheduler.main import scheduler


async def text_messages(query: str, **kwargs):
    texts = {
        "init": "⚠️ Добавление каналов происходит по 1 за раз. ⚠️\n"
                "👉 Пожалуйста введите адрес добавляемого канала.\n\n"
                "Пример public канала: https://t.me/test_parser_news",
        "process_url": "Подтвердите введенные данные: \n"
                       f"{kwargs.get('url', None)}",
        "filed_process_url": "В ссылке должно быть https://t.me, попробуйте еще раз. \n"
                             "Пример privat канала: https://t.me/+koUUZxSej2NjNDhi\n"
                             "Пример public канала: https://t.me/test_parser_news",
        "process_finish": f"🎉 Группа {kwargs.get('url', None)} успешно добавлена, в ближайшее время придут "
                          "сообщения на модерацию.",
        "process_finish_error": f"Группа уже существует в базе. 🤷 "

    }

    return texts[query]


class UrlAction(StatesGroup):
    url = State()
    finish = State()


class InterfaceFsmUrl:

    @staticmethod
    async def init_action_url(call: CallbackQuery, state: FSMContext):
        await state.set_state(UrlAction.url)

        msg_entity = await call.message.answer(text=await text_messages(query="init"))
        await state.update_data(msg_id=msg_entity.message_id)

    @staticmethod
    async def process_url(message: Message, state: FSMContext):
        await state.update_data(url=message.text)
        view = View(message)
        data = await state.get_data()

        await view.delete_message()
        await view.delete_message(data['msg_id'])

        data = await state.get_data()
        await state.set_state(UrlAction.finish)
        msg_entity = await message.answer(text=await text_messages(query="process_url", url=data.get('url')),
                                          reply_markup=yes_no())
        await state.update_data(msg_id=msg_entity.message_id)

    @staticmethod
    async def filed_process_url(message: Message, state: FSMContext):
        view = View(message)
        data = await state.get_data()

        await view.delete_message()
        await view.delete_message(data['msg_id'])

        msg_entity = await message.answer(text=await text_messages(query="filed_process_url"))
        await state.update_data(msg_id=msg_entity.message_id)

    @staticmethod
    async def process_finish(message: Message, state: FSMContext):
        db = Database()
        answer = await state.update_data(answer=message.text.casefold())
        view = View(message)
        data = await state.get_data()

        await view.delete_message()
        await view.delete_message(data['msg_id'])

        if answer.get('answer') == "да":
            data = await state.get_data()

            channel_data = ChannelData(link=data['url'])

            if not await db.get_channel_by_link(link=data['url']):
                scheduler.add_job(db.add_channel, kwargs={"channel_data": channel_data})

                await view.print_message(text=await text_messages(query="process_finish", url=data.get('url')),
                                         kb=admin_menu)
            else:
                await view.print_message(text=await text_messages(query="process_finish_error", url=data.get('url')),
                                         kb=admin_menu)
            await state.clear()
        else:
            await state.set_state(UrlAction.url)
            msg_entity = await message.answer(text=await text_messages(query="init"),
                                              reply_markup=ReplyKeyboardRemove())
            await state.update_data(msg_id=msg_entity.message_id)
