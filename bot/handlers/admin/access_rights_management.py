from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from bot.keyboards.inline import admin_rights_menu, admin_menu, channel_back_to_admin_menu
from bot.keyboards.reply import yes_no
from bot.view.main import View
from database.methods.main import Database
from scheduler.main import scheduler


class AccessAction(StatesGroup):
    admin_id = State()
    finish = State()


async def text_messages(query: str, **data):
    messages = {
        "init": "Введите Telegram ID пользователя: \n\nПример: 123456789",
        "failed_admin": "Допускаются только цифры, попрубуйте ще раз.",
        "finish_process": f"Проверьте ID: {data.get('id', 0)} и поддтвердите.",
        "menu": "Выбирите действие: ",
        "finish_complete_add": f"Привет {data.get('name', 'Noname')}.\nПрава доступа: Администратор\n\n"
                               f"Вы удачно добавили админитсратора,"
                               f" с ID: {data.get('id', 0)}",
        "finish_complete_delete": f"Привет {data.get('name', 'Noname')}.\n\nПрава доступа: Администратор\n\n"
                                  f"Вы удачно удалили админитсратора,"
                                  f" с ID: {data.get('id', 0)}",
    }

    return messages.get(query, "Command not found")


class AccessManagementFSM:

    @staticmethod
    async def init_action(state: FSMContext, type_: str, context: CallbackQuery):
        view = View(context=context)
        await state.set_state(AccessAction.admin_id)
        await state.update_data(type=type_, last_msg_id=context.message.message_id)

        await view.print_message(text=await text_messages(query="init"), kb=channel_back_to_admin_menu)

    @staticmethod
    async def admin_id_process(message: Message, state: FSMContext):
        await state.set_state(AccessAction.finish)
        id_ = int(message.text)
        view = View(message)

        await view.delete_message()

        await state.update_data(id_=id_)
        msg_entity = await message.answer(text=await text_messages(query="finish_process", id=id_),
                                          reply_markup=yes_no())

        await state.update_data(msg_id=msg_entity.message_id)

    @staticmethod
    async def failed_admin_id_process(message: Message, state: FSMContext):
        view = View(message)
        data = await state.get_data()
        await view.delete_message()
        await view.delete_message(data['msg_id'])
        await view.print_message(text=await text_messages(query="failed_admin"), kb=channel_back_to_admin_menu)

    @staticmethod
    async def finish_process(message: Message, state: FSMContext):
        await state.update_data(answer=message.text.casefold())
        data = await state.get_data()
        entity = AccessManagement()
        view = View(message)

        await view.delete_message(data['msg_id'])
        await view.delete_message()

        if data['answer'] == "да":

            if data['type'] == "add":
                await entity.add_admin(id_=int(data['id_']))
                await view.print_message(text=await text_messages(query="finish_complete_add", id=data['id_'],
                                                                  name=message.from_user.full_name), kb=admin_menu)
            elif data['type'] == "delete":
                await entity.delete_admin(id_=int(data['id_']))
                await view.print_message(text=await text_messages(query="finish_complete_delete", id=data['id_'],
                                                                  name=message.from_user.full_name), kb=admin_menu)
            else:
                print("error")

            await state.clear()
        else:
            await state.set_state(AccessAction.admin_id)
            await message.answer(text=await text_messages(query="init"))


class AccessManagement:
    def __init__(self, context: CallbackQuery = None):
        self.context = context
        self.database = Database()

    async def _init_add_admin(self, state):
        await AccessManagementFSM.init_action(type_="add", context=self.context, state=state)

    async def _init_delete_admin(self, state):
        await AccessManagementFSM.init_action(type_="delete", context=self.context, state=state)

    async def _delete_all_admin(self):
        admins = await self.database.get_all_admin()
        view = View(self.context)
        for admin_id in admins:
            update_access_admin = {
                "is_admin": False
            }

            await self.database.update_user(user_id=admin_id, update_data=update_access_admin)
        await view.print_message(text="Все администраторы были удалены.", kb=admin_menu)

    async def add_admin(self, id_: int):
        update_data = {
            "is_admin": True
        }
        scheduler.add_job(self.database.update_user, kwargs={"user_id": id_, "update_data": update_data})

    async def delete_admin(self, id_: int):
        update_data = {
            "is_admin": False
        }
        scheduler.add_job(self.database.update_user, kwargs={"user_id": id_, "update_data": update_data})

    async def command_router(self, state: FSMContext):
        callback_data = self.context.data.split("_")
        if len(callback_data) > 3:

            match callback_data[2]:
                case "add":
                    await self._init_add_admin(state=state)
                case "delete":
                    await self._init_delete_admin(state=state)
                case "delete:all":
                    await self._delete_all_admin()
                case "_":
                    return "Command not find"
        else:
            view = View(self.context)
            await view.print_message(text=await text_messages(query="menu"), kb=admin_rights_menu)
