from database.methods.post import add_item_autoincrement, \
    add_transaction_autoincrement
from database.methods.get import get_channel_by_id, \
    get_posts_by_channel_id, \
    get_all_users, get_user_by_id, get_all_channels, get_channel_by_link, get_posts_for_compare
from database.methods.put import update_post_by_post_id, update_user_by_id, update_channel_by_id
from database.models.channel import ChannelData, Channel
from database.models.media import Media
from database.models.posts import Post, PostData
from database.models.user import UserData, User
from settings.config import settings
from database.main import Base


class Database:

    async def add_channel(self, channel_data: ChannelData):
        id_ = int(await add_item_autoincrement(Channel(channel_data)))
        channel_data.id = id_

        return channel_data

    async def update_channel(self, channel_id: int, channel_data: dict):
        await update_channel_by_id(channel_id, data=channel_data)

    async def get_channel(self, channel_id: int):
        return await get_channel_by_id(cid=channel_id)

    async def get_channel_by_link(self, link):
        return [item.id for item in await get_channel_by_link(link=link)]

    async def get_channels(self):
        return [ChannelData(id=item.id,
                            link=item.link,
                            name=item.name,
                            description=item.description,
                            user_count=item.user_count,
                            telegram_channel_id=item.telegram_channel_id) for item in await get_all_channels()]

    async def add_users(self, users: list[UserData]):
        return await add_transaction_autoincrement(users)

    async def add_user(self, user: UserData):
        return await add_item_autoincrement(User(user))

    async def update_user(self, user_id: int, update_data: dict):
        await update_user_by_id(user_id=user_id, data=update_data)

    async def get_user(self, user_id: int) -> UserData:

        user = {item.id: {
            "id": item.id,
            "name": item.name,
            "phone": item.phone,
            "email": item.email,
            "active_msg_id": item.active_msg_id,
            "is_admin": item.is_admin,
            "update_at": item.update_at
        } for item in await get_user_by_id(user_id=user_id)}

        return UserData.dict_to_user_data(data=user[user_id])

    async def check_user(self, user_id: int) -> bool:
        return (False, True)[len([item.id for item in await get_user_by_id(user_id=user_id)]) != 0]

    async def add_posts(self, items: list[Base]):
        return await add_transaction_autoincrement(items)

    async def add_post(self, item: PostData) -> int | None:
        return await add_item_autoincrement(Post(item))

    async def update_posts(self, items: list[dict]):
        for item in items:
            for k, v in item.items():
                await update_post_by_post_id(post_id=k, data=v.to_dict())

    async def update_post(self, post_id: int, data: dict):
        await update_post_by_post_id(post_id=post_id, data=data)

    async def get_posts_by_channel_id(self, channel_id: int):
        return await get_posts_by_channel_id(channel_id)

    async def get_posts_for_compare_(self, channel_id: int, limit: int = settings.telegram_parser.max_update_post):
        return await get_posts_for_compare(cid=channel_id, limit=limit)

    async def get_new_post_by_channel_id(self, channel_id: int):
        return await get_posts_by_channel_id(channel_id)

    async def get_all_post_id_by_channel_id(self, channel_id: int) -> list[int]:
        return [item.id for item in await get_posts_by_channel_id(channel_id)]

    async def get_all_users(self):
        return await get_all_users()
