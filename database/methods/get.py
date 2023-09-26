from sqlalchemy import and_, desc
from sqlalchemy.future import select
from database.main import async_session_maker
from database.models.channel import Channel
from database.models.media import Media
from database.models.modify_post import ModifyPost
from database.models.openai import Openai
from database.models.posts import Post
from database.models.user import User


async def get_all_channels():
    async with async_session_maker() as s:
        q = select(Channel)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_channel_by_id(cid: int):
    async with async_session_maker() as s:
        q = select(Channel).filter(Channel.id == cid)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_channel_by_link(link: int):
    async with async_session_maker() as s:
        q = select(Channel).filter(Channel.link == link)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_posts_by_channel_id(cid: int):
    async with async_session_maker() as s:
        q = select(Post).filter(Post.channel_id == cid)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_posts_for_openai():
    async with async_session_maker() as s:
        q = select(Post).filter(and_(Post.state == "new",
                                     Post.published == False,
                                     Post.reject == False))
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_posts_for_approve_post():
    async with async_session_maker() as s:
        q = select(ModifyPost).filter(ModifyPost.approve_state == "new")
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_posts_for_published_post(message_id: int, channel_id: int):
    async with async_session_maker() as s:
        q = select(Post).filter(and_(Post.message_id == message_id,
                                     Post.channel_id == channel_id,
                                     Post.modified_text != "none"))
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_post(message_id: int, channel_id: int):
    async with async_session_maker() as s:
        q = select(Post).filter(and_(Post.message_id == message_id,
                                     Post.channel_id == channel_id))
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_mod_post(post_id: int):
    async with async_session_maker() as s:
        q = select(ModifyPost).filter(ModifyPost.id == post_id)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_posts_for_compare(cid: int):
    async with async_session_maker() as s:
        q = select(Post).filter(Post.channel_id == cid).order_by(Post.message_id)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_all_users():
    async with async_session_maker() as s:
        q = select(User)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_all_admin_():
    async with async_session_maker() as s:
        q = select(User).filter(User.is_admin == True)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_media_for_delete():
    async with async_session_maker() as s:
        q = select(Media).filter(Media.file_name == "delete")
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_prompt():
    async with async_session_maker() as s:
        q = select(Openai)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_user_by_id(user_id: int):
    async with async_session_maker() as s:
        q = select(User).filter(User.id == user_id)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_photo(channel_id: int, message_id: int):
    async with async_session_maker() as s:
        q = select(Media).filter(and_(Media.channel_id == channel_id, Media.post_id == message_id))
        data = await s.execute(q)
        curr = data.scalars()
    return curr
