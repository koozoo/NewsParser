from aiogram import Dispatcher
from .admin.admin_handlers import register_admin_handlers
from .user.user_handlers import register_user_handlers
from .commands.commands import register_commands_handler


async def register_handlers(dp: Dispatcher):
    await register_commands_handler(dp)
    await register_user_handlers(dp)
    await register_admin_handlers(dp)
