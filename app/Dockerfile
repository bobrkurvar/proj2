FROM python:3.11-slim

WORKDIR /web

COPY ./req.txt .

RUN pip install --no-cache-dir -r app_req.txt

COPY ./app /web/app
COPY ./db /web/db

CMD ["uvicorn", "main_app:app", "--host", "0.0.0.0", "--port", "8000"]