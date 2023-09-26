from aiogram.types import CallbackQuery, Message

from services.cache.cache import Cache


class View:

    def __init__(self, context: CallbackQuery | Message):
        self.context = context
        self.chat_id = context.from_user.id
        self.cache = Cache()

    async def print_message(self, text: str, kb) -> None:
        user = await self.cache.get_user(user_id=self.context.from_user.id)

        try:
            await self.context.bot.edit_message_text(chat_id=self.chat_id, message_id=user.active_msg_id, text=text,
                                                     reply_markup=kb(user.active_msg_id))
        except Exception as e:
            print(e)
            await self.delete_message(user.active_msg_id)
            message_data = await self.context.bot.send_message(chat_id=self.chat_id, text=text,
                                                               reply_markup=kb(user.active_msg_id + 1))

            user.active_msg_id = message_data.message_id
            await self.cache.update_user(user=user)

    async def delete_message(self, msg_id: int | None = None) -> None:

        if msg_id is not None:
            try:
                await self.context.bot.delete_message(chat_id=self.chat_id, message_id=msg_id)
            except Exception as e:
                print(e)
        else:
            try:
                if isinstance(self.context, Message):
                    await self.context.delete()
                else:
                    await self.context.message.delete()

            except Exception as e:
                print(e)
