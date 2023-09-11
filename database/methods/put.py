import logging
from datetime import datetime

from sqlalchemy import update

from database.main import async_session_maker
from database.models.posts import Post


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
                         f"in data base {datetime.now()}")
