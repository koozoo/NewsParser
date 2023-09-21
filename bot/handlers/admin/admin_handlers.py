import logging
from aiogram import Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from .add_channel import InterfaceFsmUrl, UrlAction
from .aprove_post import ApprovePost
from .access_rights_management import AccessManagement, AccessManagementFSM, AccessAction


async def init_approve(call: CallbackQuery):
    entity = ApprovePost(callback=call.data, context=call)
    await entity.type_router()


async def init_access_rights(call: CallbackQuery, state: FSMContext):
    entity = AccessManagement(context=call)
    await state.set_data({"init": "test"})
    await entity.command_router(state=state)


async def register_admin_handlers(dp: Dispatcher):
    logging.info("REGISTER ALL ADMIN HANDLERS")

    dp.callback_query.register(init_approve, F.data.startswith("MESSAGE"))
    dp.callback_query.register(init_access_rights, F.data.startswith("ADMIN_rights"))

    # FSM ADD ADMIN
    dp.message.register(AccessManagementFSM.failed_admin_id_process, AccessAction.admin_id,
                        lambda msg: not msg.text.isdigit())
    dp.message.register(AccessManagementFSM.admin_id_process, AccessAction.admin_id)
    dp.message.register(AccessManagementFSM.finish_process, AccessAction.finish,
                        lambda msg: msg.text.casefold() in ["да", "нет"])

    # FSM URL EVENT
    dp.callback_query.register(InterfaceFsmUrl.init_action_url,
                               F.data.startswith("ADMIN_add"))

    dp.message.register(InterfaceFsmUrl.filed_process_url,
                        UrlAction.url,
                        lambda msg: "https://t.me" not in msg.text)
    dp.message.register(InterfaceFsmUrl.process_url,
                        UrlAction.url,
                        lambda msg: "https://t.me" in msg.text)
    dp.message.register(InterfaceFsmUrl.process_finish,
                        UrlAction.finish,
                        lambda msg: msg.text.casefold() in ["да", "нет"])
