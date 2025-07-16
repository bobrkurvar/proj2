FROM python:3.11-slim

WORKDIR /bot

COPY ./bot_req.txt .

RUN pip install --no-cache-dir -r bot_req.txt

COPY . .

CMD ["py", "-m", "main_bot"]