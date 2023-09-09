from bot.database.methods.post import add_item_autoincrement, \
    add_transaction_autoincrement
from bot.database.methods.get import get_channel_by_id, \
    get_posts_by_channel_id, \
    get_all_users_in_channel_by_cid, get_all_users, get_new_msg_by_cin
from bot.database.methods.put import update_task_by_id, update_task_item_by_id, update_post_by_post_id
from bot.database.models.channel import ChannelData, Channel
from bot.database.models.posts import Post
from bot.database.models.task_item import TaskItem
from bot.database.models.user import UserData
from bot.database.models.user_channel import UserChannel
from bot.parser_data.utils import convert_dict_to_task_item


class Database:

    def __init__(self, uid: int = None):
        self.uid = uid

    async def add_task_item(self, task_item: dict):

        return {"status": 200,
                "task_item_id": int(await add_item_autoincrement(
                    TaskItem(await convert_dict_to_task_item(task_item)))),
                "raw_data": task_item
                }

    async def update_task(self, task_id: int, update_data: dict):

        await update_task_by_id(task_id=task_id, data=update_data)

    async def update_task_item(self, task_item_id: int, update_data: dict):

        await update_task_item_by_id(task_item_id=task_item_id,
                                     data=update_data)

    async def add_channel(self, channel_data: ChannelData, channel: Channel):
        new_id = int(await add_item_autoincrement(channel))

        channel_data.id = new_id

        return {"status": 200,
                "channel_id": new_id,
                "raw_data": channel_data
                }

    async def get_channel(self, channel_id: int):
        return await get_channel_by_id(cid=channel_id)

    async def add_users(self, users: list[UserData]):
        return await add_transaction_autoincrement(users)

    async def add_user_channel(self, items: list[UserChannel]):
        return await add_transaction_autoincrement(items)

    async def add_posts(self, items: list[Post]):
        return await add_transaction_autoincrement(items)

    async def update_posts(self, items: list[dict]):
        for item in items:
            for k, v in item.items():
                await update_post_by_post_id(post_id=k, data=v.to_dict())

    async def update_post(self, post_id: int, data: dict):
        await update_post_by_post_id(post_id=post_id, data=data)

    async def get_posts_by_channel_id(self, channel_id: int):
        return await get_posts_by_channel_id(channel_id)

    async def get_all_users(self):
        return await get_all_users()

    async def get_all_users_in_channel(self, cid: int):
        return await get_all_users_in_channel_by_cid(cid=cid)

    async def get_new_messages_by_channel_id(self, channel_id: int) -> dict:
        return {item.id: {
            "channel_id": item.channel_id,
            "id": item.id,
            "message_id": item.message_id,
            "text": item.text,
            "views_count": item.views_count,
            "reactions_count": item.reactions_count,
            "comments_channel_id": item.comments_channel_id,
            "type": item.type
        } for item in await get_new_msg_by_cin(cin=channel_id)
        }
