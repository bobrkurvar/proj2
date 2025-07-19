FROM python:3.11-slim

WORKDIR /proj2

COPY ./req.txt .

RUN pip install --no-cache-dir -r req.txt

COPY ./main_bot.py /proj2/
COPY ./bot /proj2/bot
COPY ./core /proj2/core

CMD ["python", "main_bot.py"]