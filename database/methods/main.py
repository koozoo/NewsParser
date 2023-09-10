from database.methods.post import add_item_autoincrement, \
    add_transaction_autoincrement
from database.methods.get import get_channel_by_id, \
    get_posts_by_channel_id, \
    get_all_users, get_new_msg_by_cin
from database.methods.put import update_task_by_id, update_task_item_by_id, update_post_by_post_id
from database.models.channel import ChannelData, Channel
from database.models.posts import Post
from database.models.task_item import TaskItem, TaskItemData
from database.models.user import UserData


class Database:

    async def add_task_item(self, task_item: TaskItemData):

        return {"status": 200,
                "task_item_id": int(await add_item_autoincrement(
                    TaskItem(task_item))),
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
