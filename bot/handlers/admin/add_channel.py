from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from bot.keyboards.reply import yes_no
from bot.handlers.utils import is_email


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
                          "сообщения на модерацию."

    }

    return texts[query]


class UrlAction(StatesGroup):
    url = State()
    finish = State()


class InterfaceFsmUrl:

    @staticmethod
    async def init_action_url(call: CallbackQuery, state: FSMContext):
        await state.set_state(UrlAction.url)

        await call.message.answer(text=await text_messages(query="init"))

    @staticmethod
    async def process_url(message: Message, state: FSMContext):
        await state.update_data(url=message.text)

        await InterfaceFsmUrl.delete_message(message)

        data = await state.get_data()
        await state.set_state(UrlAction.finish)
        await message.answer(text=await text_messages(query="process_url", url=data.get('url')),
                             reply_markup=yes_no())

    @staticmethod
    async def filed_process_url(message: Message):
        await InterfaceFsmUrl.delete_message(message)
        await message.answer(text=await text_messages(query="filed_process_url"))

    @staticmethod
    async def process_finish(message: Message, state: FSMContext):

        answer = await state.update_data(answer=message.text.casefold())
        await InterfaceFsmUrl.delete_message(message)

        if answer.get('answer') == "да":
            data = await state.get_data()
            # добавить в бд новый канал
            await message.answer(text=await text_messages(query="process_finish", url=data.get('url')),
                                 reply_markup=ReplyKeyboardRemove())
            await state.clear()
        else:
            await state.set_state(UrlAction.url)
            await message.answer(text=await text_messages(query="init"),
                                 reply_markup=ReplyKeyboardRemove())

    @staticmethod
    def check_email(text):
        return (False, True)[is_email(text) is not None]

    @staticmethod
    async def delete_message(context: Message | CallbackQuery):

        try:
            await context.delete()
        except Exception as e:
            print(e)
            await context.message.delete()
