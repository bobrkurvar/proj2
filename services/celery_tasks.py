from celery import Celery

app = Celery('celery_tasks', broker="redis://localhost:6379/0")
