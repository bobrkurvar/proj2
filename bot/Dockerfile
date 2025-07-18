FROM python:3.11-slim

WORKDIR /bot

COPY ./req.txt .

RUN pip install --no-cache-dir -r bot_req.txt

COPY ./bot /bot

CMD ["py", "-m", "main_bot"]