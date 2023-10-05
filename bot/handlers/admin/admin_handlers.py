import logging
from aiogram import Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from .add_channel import InterfaceFsmUrl, UrlAction
from .aprove_post import ApprovePost, EditAction, EditPost
from .access_rights_management import AccessManagement, AccessManagementFSM, AccessAction
from .delete_channel import InterfaceFsmDelete, DeleteAction
from .update_prompt import PromptManagementFSM, PromptAction
from .channel_ import ChannelMenu, GetChannelAction, InterfaceGetChannel
from .update_prompt import Prompt


async def init_approve(call: CallbackQuery, state: FSMContext | None):
    if isinstance(state, FSMContext):
        entity = ApprovePost(callback=call.data, context=call, state=state)
        await entity.type_router()
    else:
        entity = ApprovePost(callback=call.data, context=call)
        await entity.type_router()


async def init_access_rights(call: CallbackQuery, state: FSMContext):
    entity = AccessManagement(context=call)
    await entity.command_router(state=state)


async def init_update_prompt(call: CallbackQuery, state: FSMContext):
    entity = Prompt(context=call)
    await entity.init_prompt(state=state)


async def init_channel(call: CallbackQuery, state: FSMContext):
    channel_menu_entity = ChannelMenu(context=call)
    await channel_menu_entity.start(state=state)


async def close(call: CallbackQuery):
    await call.message.delete()


async def register_admin_handlers(dp: Dispatcher):
    logging.info("REGISTER ALL ADMIN HANDLERS")

    dp.callback_query.register(init_approve, F.data.startswith("MESSAGE"))
    dp.callback_query.register(init_access_rights, F.data.startswith("ADMIN_rights"))
    dp.callback_query.register(init_update_prompt, F.data.startswith("PROMPT"))
    dp.callback_query.register(init_channel, F.data.startswith("CHANNEL"))
    dp.callback_query.register(close, F.data.startswith("CLOSE"))

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

    # FSM DELETE EVENT
    dp.callback_query.register(InterfaceFsmDelete.init_action_delete,
                               F.data.startswith("ADMIN_delete"))
    dp.message.register(InterfaceFsmDelete.filed_process_delete,
                        DeleteAction.delete,
                        lambda msg: not msg.text.isdigit())

    dp.message.register(InterfaceFsmDelete.process_delete,
                        DeleteAction.delete,
                        lambda msg: msg.text.isdigit())

    dp.message.register(InterfaceFsmDelete.process_finish,
                        DeleteAction.finish,
                        lambda msg: msg.text.casefold() in ["да", "нет"])

    # PROMPT UPDATE
    dp.callback_query.register(init_update_prompt,
                               F.data.startswith("PROMPT"))

    dp.message.register(PromptManagementFSM.prompt_process,
                        PromptAction.pr,
                        lambda msg: msg.text)

    dp.message.register(PromptManagementFSM.finish_process,
                        PromptAction.finish,
                        lambda msg: msg.text.casefold() in ["да", "нет"])

    # EDIT POST

    dp.message.register(EditPost.edit_process,
                        EditAction.edit,
                        lambda msg: msg.text)

    dp.message.register(EditPost.finish_process,
                        EditAction.finish,
                        lambda msg: msg.text.casefold() in ["да", "нет"])

    # FSM FIND URL EVENT
    dp.message.register(InterfaceGetChannel.filed_link_process,
                        GetChannelAction.link,
                        lambda msg: "https://t.me" not in msg.text)
    dp.message.register(InterfaceGetChannel.link_process,
                        GetChannelAction.link,
                        lambda msg: "https://t.me" in msg.text)
    dp.message.register(InterfaceGetChannel.finish_process,
                        GetChannelAction.finish,
                        lambda msg: msg.text.casefold() in ["да", "нет"])
