import logging
import datetime as dt

from sqlalchemy import update

from database.main import async_session_maker
from database.models.channel import Channel
from database.models.modify_post import ModifyPost
from database.models.posts import Post
from database.models.user import User


async def update_post_by_post_id(post_id: int, data: dict):

    async with async_session_maker() as s:

        async with s.begin():
            q = update(
                Post)\
                .filter(Post.id == post_id)\
                .values(data)\
                .execution_options(synchronize_session="fetch")
            await s.execute(q)
            await s.commit()

            logging.info(f"item update POST ID: {post_id}"
                         f"in data base {dt.datetime.utcnow()}")


async def update_modify_post_by_post_id(post_id: int, data: dict):

    async with async_session_maker() as s:

        async with s.begin():
            q = update(
                ModifyPost)\
                .filter(ModifyPost.id == post_id)\
                .values(data)\
                .execution_options(synchronize_session="fetch")
            await s.execute(q)
            await s.commit()

            logging.info(f"item update POST ID: {post_id}"
                         f"in data base {dt.datetime.utcnow()}")


async def update_user_by_id(user_id: int, data: dict):

    async with async_session_maker() as s:

        async with s.begin():
            q = update(
                User)\
                .filter(User.id == user_id)\
                .values(data)\
                .execution_options(synchronize_session="fetch")
            await s.execute(q)
            await s.commit()

            logging.info(f"Update USER: ID: {user_id}"
                         f"in data base {dt.datetime.utcnow()}")


async def update_channel_by_id(channel_id: int, data: dict):

    async with async_session_maker() as s:

        async with s.begin():
            q = update(
                Channel)\
                .filter(Channel.id == channel_id)\
                .values(data)\
                .execution_options(synchronize_session="fetch")
            await s.execute(q)
            await s.commit()

            logging.info(f"Update Channel: ID: {channel_id}"
                         f"in data base {dt.datetime.utcnow()}")