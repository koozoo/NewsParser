from celery import Celery
from settings.config import settings

if settings.redis.pass_ is not None and settings.redis.pass_ != "":
    openai_worker = Celery("openai_worker", broker=f'redis://{settings.redis.pass_}@{settings.redis.host}:{settings.redis.port}/1',
                           backend=f'redis://{settings.redis.pass_}@{settings.redis.host}:{settings.redis.port}/1',
                           include=['worker.tasks']
                           )
else:
    openai_worker = Celery("openai_worker", broker=f'redis://{settings.redis.host}:{settings.redis.port}/1',
                           backend=f'redis://{settings.redis.host}:{settings.redis.port}/1',
                           include=['worker.tasks']
                           )

openai_worker.autodiscover_tasks()
openai_worker.conf.timezone = 'Europe/Moscow'
