import logging
from aiogram import Dispatcher, F
from .add_channel import InterfaceFsmUrl, UrlAction


async def register_admin_handlers(dp: Dispatcher):
    logging.info("REGISTER ALL ADMIN HANDLERS")

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


