import logging
from datetime import datetime

from sqlalchemy import update

from database.main import async_session_maker
from database.models.posts import Post
from database.models.task import Task
from database.models.task_item import TaskItem


async def update_task_by_id(task_id: int, data: dict):
    async with async_session_maker() as s:
        async with s.begin():

            stmt = update(Task).\
                where(Task.id == task_id).\
                values(data).\
                execution_options(synchronize_session="fetch")

            await s.execute(stmt)
            await s.commit()
            logging.info(f"item update task ID: {task_id}"
                         f"in data base {datetime.now()}")


async def update_task_item_by_id(task_item_id: int, data: dict):
    async with async_session_maker() as s:
        async with s.begin():
            q = update(
                TaskItem)\
                .filter(TaskItem.id == task_item_id)\
                .values(data)\
                .execution_options(synchronize_session="fetch")
            await s.execute(q)
            await s.commit()
            logging.info(f"item update task_item ID: {task_item_id}"
                         f"in data base {datetime.now()}")


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
