FROM python:3.11-slim

WORKDIR /proj2

COPY ./req.txt .

RUN pip install --no-cache-dir -r req.txt

COPY ./app /proj2/app
COPY ./db /proj2/db
COPY ./main_app.py /proj2/
COPY ./core /proj2/core
COPY ./alembic.ini /proj2/
COPY ./migrations /proj2/migrations

CMD ["bash", "-c", "alembic upgrade head && uvicorn main_app:app --host 0.0.0.0 --port 8000"]