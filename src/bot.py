#########################
#                       #
#.  написан на telebot. #
#                       #
#########################


import os
import random
import time
from collections import deque
import telebot                  #если горит ошибка не трогай
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Используем переменные окружения для токена и ID чата
API_TOKEN = os.getenv('BOT_TOKEN')  # Замените на 'BOT_TOKEN' если у вас другой
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(API_TOKEN)

# Настройки реакции на флуд
MESSAGE_THRESHOLD = 60  # Количество сообщений для реакции
TIMEOUT = 60  # Время в секундах для сброса массива сообщений
FRASE = "Ле, че началось да"

# Ответы на ключевые слова
responses = {
    "ало": "Хуем по лбу не дало?",
    "че": "ниче",
    "работай": "ди нах"
}

# Массив для хранения сообщений
messages = deque()

# Функция для отправки приветственного сообщения при запуске
def send_welcome_message():
    bot.send_message(CHAT_ID, 'Бот запущен.')

# Функция для обработки текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global messages

    # Ответы на ключевые слова
    message_text = message.text.lower()
    for keyword, response in responses.items():
        if keyword in message_text:
            bot.reply_to(message, response)
            break

    # Приветствие Ивана Владимировича
    if "доброе утро" in message_text and message.from_user.id == 786761078:
        bot.reply_to(message, "Доброе утро, Иван Владимирович")

    # Реакция на флуд
    messages.append((message.chat.id, message.message_id))

    if len(messages) >= MESSAGE_THRESHOLD:
        random_message = random.choice(messages)
        chat_id, message_id = random_message
        bot.send_message(chat_id, FRASE, reply_to_message_id=message_id)
        messages.clear()

# Функция для сброса сообщений каждые TIMEOUT секунд
def message_reset_loop():
    global messages
    while True:
        time.sleep(TIMEOUT)
        messages.clear()

if __name__ == '__main__':
    send_welcome_message()
    import threading
    threading.Thread(target=message_reset_loop).start()  # Запускаем сброс сообщений в отдельном потоке
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        bot.send_message(CHAT_ID, 'Бот остановлен.')
        print("Бот остановлен.")
