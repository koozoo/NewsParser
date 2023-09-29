from database.methods.post import add_item_autoincrement, \
    add_transaction_autoincrement
from database.methods.get import (get_channel_by_id, \
                                  get_posts_by_channel_id, \
                                  get_all_users, get_user_by_id, get_all_channels,
                                  get_channel_by_link, get_posts_for_compare, get_posts_for_openai,
                                  get_posts_for_approve_post, get_posts_for_published_post, get_photo, get_mod_post,
                                  get_post, get_all_admin_, get_prompt, get_mod_post_by_message_id_and_channel_id)
from database.methods.put import (update_post_by_post_id, update_user_by_id, update_channel_by_id,
                                  update_modify_post_by_post_id, update_media_by_media_id, update_prompt)
from database.methods.delete import delete_channel_by_id
from database.models.channel import ChannelData, Channel
from database.models.media import MediaData
from database.models.modify_post import ModifyPostData
from database.models.openai import OpenaiData
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

    async def add_any_item(self, item: Base):
        return await add_item_autoincrement(item)

    async def update_posts(self, items: list[dict]):
        for item in items:
            for k, v in item.items():
                await update_post_by_post_id(post_id=k, data=v.to_dict())

    async def update_post(self, post_id: int, data: dict):
        await update_post_by_post_id(post_id=post_id, data=data)

    async def update_media(self, media_id: int, data: dict):
        await update_media_by_media_id(media_id=media_id, data=data)

    async def get_posts_by_channel_id(self, channel_id: int):
        return await get_posts_by_channel_id(channel_id)

    async def get_posts_for_compare_(self, channel_id: int):
        return await get_posts_for_compare(cid=channel_id)

    async def get_new_post_by_channel_id(self, channel_id: int):
        return await get_posts_by_channel_id(channel_id)

    async def get_posts_for_openai(self):
        return {"posts": [PostData(id=post.id,
                                   text=post.text,
                                   state="pending",
                                   channel_id=post.channel_id,
                                   type=post.type,
                                   message_id=post.message_id).to_dict() for post in await get_posts_for_openai()]}

    async def get_posts_for_approve(self):
        return {"posts": [ModifyPostData(id=post.id,
                                         text=post.text,
                                         post_id=post.post_id,
                                         approve_state="await",
                                         type=post.type,
                                         channel_id=post.channel_id) for post in await get_posts_for_approve_post()]}

    async def get_post_for_publish(self, message_id: int, channel_id: int):
        return [item.id for item in await get_posts_for_published_post(message_id=message_id,
                                                                       channel_id=channel_id)]

    async def get_post_(self, message_id: int, channel_id: int):
        return [PostData(id=item.id,
                         channel_id=item.channel_id,
                         message_id=item.message_id,
                         text=item.text,
                         modified_text=item.modified_text,
                         type=item.type) for item in await get_post(message_id=message_id, channel_id=channel_id)]

    async def get_mod_post_by_id(self, post_id: int):
        return [item.text for item in await get_mod_post(post_id=post_id)]

    async def get_all_post_id_by_channel_id(self, channel_id: int) -> list[int]:
        return [item.id for item in await get_posts_by_channel_id(channel_id)]

    async def get_all_users(self):
        return await get_all_users()

    async def update_mod_post(self, post_id: int, data: dict):
        await update_modify_post_by_post_id(post_id=post_id, data=data)

    async def get_photo_by_cin_and_msg_id(self, channel_id: int, message_id: int):
        return {"data": MediaData(type=media.type, id=media.id,
                                  post_id=media.post_id,
                                  telegram_document_id=media.telegram_document_id,
                                  channel_id=media.channel_id,
                                  photo_path=media.photo_path) for media in await get_photo(channel_id=channel_id,
                                                                                            message_id=message_id)}

    async def get_all_admin(self):
        return [item.id for item in await get_all_admin_() if item.id != settings.admin.id_]

    async def get_all_admin_with_main_admin(self):
        return [item.id for item in await get_all_admin_()]

    async def get_all_channel(self):
        return

    async def get_prompt_(self):
        return [OpenaiData(id=item.id, prompt=item.prompt, type=item.type) for item in await get_prompt()]

    async def update_prompt(self, prompt_id: int, data: dict):
        await update_prompt(prompt_id=prompt_id, data=data)

    async def delete_channel(self, channel_id: int):
        await delete_channel_by_id(channel_id=channel_id)

    async def get_mod_post_by_message_id_and_channel_id_(self, message_id: int, channel_id: int):
        return [ModifyPostData(id=item.id,
                               post_id=item.post_id,
                               text=item.text,
                               channel_id=item.channel_id,
                               approve_state=item.approve_state,
                               type=item.type)
                for item in await get_mod_post_by_message_id_and_channel_id(message_id=message_id,
                                                                            channel_id=channel_id)]
