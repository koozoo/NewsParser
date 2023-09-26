from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, Message, CallbackQuery

from bot.keyboards.inline import channel_back_to_admin_menu, admin_menu
from bot.keyboards.reply import yes_no
from bot.view.main import View
from database.methods.main import Database
from scheduler.main import scheduler


async def text_messages(query: str, **kwargs):
    print("kwarg in text message")
    texts = {
        "init": "⚠️ Каналы удаляются по 1 за раз. ⚠️\n"
                "👉 Пожалуйста введите ID удаляемого канала.\n\n"
                "Пример ID: 1",
        "process_delete": "Подтвердите введенные данные: \n"
                          f"{kwargs.get('channel_id', None)}",
        "filed_process_delete": "Вы ввли не корректные данные, вводить нужно только цифры.\n\n"
                                "Попробуейте еще раз.",
        "process_finish": f"🎉 Канал {kwargs.get('channel_id', None)} успешно удален.",
        "process_finish_error": f'Канала с ID: {kwargs.get("channel_id", None)}  нет в базе, попробуйте еще раз.'

    }

    return texts[query]


class DeleteAction(StatesGroup):
    delete = State()
    finish = State()


class InterfaceFsmDelete:

    @staticmethod
    async def init_action_delete(call: CallbackQuery, state: FSMContext):
        view = View(context=call)
        await view.print_message(await text_messages(query="init"), kb=channel_back_to_admin_menu)
        await state.set_state(DeleteAction.delete)
        # call_entity = await call.message.answer(text=)

    @staticmethod
    async def process_delete(message: Message, state: FSMContext):
        await state.update_data(channel_id=int(message.text))

        data = await state.get_data()

        await InterfaceFsmDelete.delete_message(message)

        await state.set_state(DeleteAction.finish)
        msg_entity = await message.answer(await text_messages(query="process_delete",
                                                              channel_id=data.get('channel_id')),
                                          reply_markup=yes_no())

        await state.update_data(msg_id=msg_entity.message_id)

    @staticmethod
    async def filed_process_delete(message: Message):
        view = View(message)

        await InterfaceFsmDelete.delete_message(message)
        await view.print_message(await text_messages(query="filed_process_delete"), kb=channel_back_to_admin_menu)

    @staticmethod
    async def process_finish(message: Message, state: FSMContext):
        view = View(message)
        db = Database()
        answer = await state.update_data(answer=message.text.casefold())
        data = await state.get_data()

        await InterfaceFsmDelete.delete_message(message)
        await InterfaceFsmDelete.delete_message(message, msg_id=data['msg_id'])

        if answer.get('answer') == "да":
            data = await state.get_data()
            print(data)
            if [item.id for item in await db.get_channel(channel_id=data['channel_id'])]:

                scheduler.add_job(db.delete_channel, kwargs={"channel_id": data['channel_id']})

                await view.print_message(text=await text_messages(query="process_finish",
                                                                  channel_id=data.get('channel_id')),
                                         kb=admin_menu)
                await state.clear()
            else:
                await state.set_state(DeleteAction.delete)
                await view.print_message(await text_messages(query="process_finish_error",
                                                             channel_id=data.get('channel_id')),
                                         kb=channel_back_to_admin_menu)

        else:
            await state.set_state(DeleteAction.delete)
            msg_entity = await message.answer(text=await text_messages(query="init"),
                                              reply_markup=ReplyKeyboardRemove())
            await state.update_data(msg_id=msg_entity.message_id)

    @staticmethod
    async def delete_message(context: Message | CallbackQuery, msg_id: int = None):
        if msg_id is None:
            if isinstance(context, Message):
                await context.delete()
            else:
                await context.message.delete()
        else:
            try:
                await context.bot.delete_message(chat_id=context.from_user.id, message_id=msg_id)
            except Exception as e:
                print(e)
