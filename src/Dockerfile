FROM python:3.12-slim

WORKDIR /app


COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ARG BOT_TOKEN
ARG CHAT_ID

ENV BOT_TOKEN=${BOT_TOKEN}
ENV CHAT_ID=${CHAT_ID}

CMD ["python", "bot.py"]
