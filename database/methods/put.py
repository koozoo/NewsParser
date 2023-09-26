import logging
import datetime as dt

from sqlalchemy import update

from database.main import async_session_maker
from database.models.channel import Channel
from database.models.media import Media
from database.models.modify_post import ModifyPost
from database.models.openai import Openai
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


async def update_prompt(prompt_id: int, data: dict):

    async with async_session_maker() as s:

        async with s.begin():
            q = update(
                Openai)\
                .filter(Openai.id == prompt_id)\
                .values(data)\
                .execution_options(synchronize_session="fetch")
            await s.execute(q)
            await s.commit()

            logging.info(f"item update POST ID: {prompt_id}"
                         f"in data base {dt.datetime.utcnow()}")


async def update_media_by_media_id(media_id: int, data: dict):

    async with async_session_maker() as s:

        async with s.begin():
            q = update(
                Media)\
                .filter(Media.id == media_id)\
                .values(data)\
                .execution_options(synchronize_session="fetch")
            await s.execute(q)
            await s.commit()

            logging.info(f"item update MEDIA ID: {media_id}"
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