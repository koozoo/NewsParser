from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.keyboards.inline import channel_back_to_admin_menu, admin_menu
from bot.keyboards.reply import yes_no
from bot.view.main import View
from database.methods.main import Database
from aiogram.types import CallbackQuery, Message


async def text_messages(query: str, **data):
    text_message = {
        "init": "Введите новый промпт.",
        "finish_process": "Проверьте новый промпт.\n\n"
                          f"{data.get('new_prompt', '')}",
        "admin_menu": "Вы успешно изменили промпт, новый промпт который будет использоваться"
                      f" для обработки сообщений:\n\n{data.get('new_prompt', '')}."
    }
    return text_message[query]


class PromptAction(StatesGroup):
    pr = State()
    finish = State()


class Prompt:

    def __init__(self, context: CallbackQuery):
        self._database = Database()
        self._context = context

    async def init_prompt(self, state: FSMContext):
        data = self._context.data.split("_")

        match data[1]:
            case "update":
                await PromptManagementFSM.init_update(context=self._context, state=state)
            case "add":
                ...
            case "_":
                print("error")


class PromptManagementFSM:

    @staticmethod
    async def init_update(context: CallbackQuery, state: FSMContext):
        view = View(context)
        await state.set_state(PromptAction.pr)
        await view.print_message(text=await text_messages(query="init"), kb=channel_back_to_admin_menu)

    @staticmethod
    async def prompt_process(message: Message, state: FSMContext):
        view = View(message)
        new_prompt = message.text.casefold()

        await view.delete_message()

        await state.update_data(new_prompt=new_prompt)
        await state.set_state(PromptAction.finish)

        msg_entity = await message.answer(text=await text_messages(query="finish_process", new_prompt=new_prompt),
                                          reply_markup=yes_no())
        await state.update_data(msg_id=msg_entity.message_id)

    @staticmethod
    async def finish_process(message: Message, state: FSMContext):
        view = View(message)
        answer = message.text.casefold()
        data = await state.get_data()
        db = Database()

        await view.delete_message()
        await view.delete_message(data['msg_id'])

        if answer == "да":
            pr = await db.get_prompt_()

            await db.update_prompt(prompt_id=pr[0].id, data={"prompt": data['new_prompt']})
            await view.print_message(text=await text_messages(query="admin_menu", new_prompt=data['new_prompt']),
                                     kb=admin_menu)
            await state.clear()
        else:
            await state.set_state(PromptAction.pr)
            await view.print_message(text=await text_messages(query="init"), kb=channel_back_to_admin_menu)
