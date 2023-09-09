from sqlalchemy import and_
from sqlalchemy.future import select
from bot.database.main import async_session_maker
from bot.database.models.channel import Channel
from bot.database.models.posts import Post
from bot.database.models.task import Task
from bot.database.models.task_item import TaskItem
from bot.database.models.user import User
from bot.database.models.user_channel import UserChannel


async def get_task_by_uid(uid: int, status: str = "create"):
    async with async_session_maker() as s:
        q = select(Task).filter(and_(Task.user_id == uid,
                                     Task.status == status))
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_task_by_id(id: int):
    async with async_session_maker() as s:
        q = select(Task).filter(Task.id == id)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_task_item_by_id(id: int):
    async with async_session_maker() as s:
        q = select(TaskItem).filter(TaskItem.id == id)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


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


async def get_all_users_in_channel_by_cid(cid: int):
    async with async_session_maker() as s:
        q = select(UserChannel).filter(UserChannel.channel_id == cid)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_new_msg_by_cin(cin: int):
    async with async_session_maker() as s:
        q = select(Post).filter(and_(Post.channel_id == cin, Post.state == "new", Post.type == "Text"))
        data = await s.execute(q)
        curr = data.scalars()
    return curr
