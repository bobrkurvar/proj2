# Stage 1: базовый с зависимостями
FROM python:3.11-slim AS base

WORKDIR /proj2

COPY ./req.txt ./req.txt
RUN pip install --no-cache-dir -r req.txt

# Stage 2: бот (aiogram)
FROM base AS bot

COPY ./main_bot.py ./main_bot.py
COPY ./bot ./bot
COPY ./core ./core

CMD ["python", "main_bot.py"]

# Stage 3: fastapi приложение
FROM base AS app

COPY ./main_app.py ./main_app.py
COPY ./app ./app
COPY ./db ./db
COPY ./core ./core
COPY ./alembic.ini ./alembic.ini
COPY ./migrations ./migrations

CMD ["bash", "-c", "alembic upgrade head && uvicorn main_app:app --host 0.0.0.0 --port 8000"]

# Stage 4: celery (worker + beat)
FROM base AS celery

COPY ./services ./services
COPY ./core ./core
COPY ./bot ./bot
COPY ./main_bot.py ./main_bot.py

WORKDIR /proj2

CMD ["bash", "-c", "celery -A services.celery_tasks worker --loglevel=info & celery -A services.celery_tasks beat --loglevel=info & wait"]

