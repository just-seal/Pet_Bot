FROM python:3.12-slim

COPY . /app
WORKDIR /app

#ADD .env /app/.env

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]