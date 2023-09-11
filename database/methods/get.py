from sqlalchemy import and_
from sqlalchemy.future import select
from database.main import async_session_maker
from database.models.channel import Channel
from database.models.posts import Post
from database.models.user import User


async def get_channel_by_id(cid: int):
    async with async_session_maker() as s:
        q = select(Channel).filter(Channel.id == cid)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_posts_by_channel_id(cid: int):
    async with async_session_maker() as s:
        q = select(Post).filter(Post.channel_id == cid)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_all_users():
    async with async_session_maker() as s:
        q = select(User)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_new_msg_by_cin(cin: int):
    async with async_session_maker() as s:
        q = select(Post).filter(and_(Post.channel_id == cin, Post.state == "new", Post.type == "Text"))
        data = await s.execute(q)
        curr = data.scalars()
    return curr
