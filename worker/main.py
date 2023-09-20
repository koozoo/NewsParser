from celery import Celery

openai_worker = Celery("openai_worker", broker='redis://localhost:6379/1',
                       backend='redis://localhost:6379/1',
                       include=['worker.tasks']
                       )

openai_worker.conf.timezone = 'Europe/Moscow'
