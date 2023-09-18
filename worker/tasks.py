import asyncio
import functools

from database.methods.main import Database
from services.openai.main import OpenAi
from .main import openai_worker


def run_async_task(func):
    @functools.wraps(func)
    def wrapper_run_async_task(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))
    return wrapper_run_async_task


async def _run_task_openai():
    database = Database()
    data = await database.get_posts_for_openai()
    entity = OpenAi(posts=data['posts'])
    await entity.init_job()


@openai_worker.task
def add_openai_job():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_run_task_openai())
