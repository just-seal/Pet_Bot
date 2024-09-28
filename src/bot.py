import os
import random
import asyncio
from collections import deque
from aiogram import Bot, Dispatcher, types
from aiogram import Router
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Используем переменные окружения для токена и ID чата
API_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)  # Убедитесь, что токен верный
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Создаем роутер
router = Router()

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

# Время работы бота
start_time = None

# Функция для отправки приветственного сообщения при запуске
async def send_welcome_message():
    await bot.send_message(CHAT_ID, 'Работаем')

# Функция для отправки сообщения о времени работы бота
async def report_work_time():
    global start_time
    while True:
        if start_time:
            elapsed_time = (asyncio.get_event_loop().time() - start_time) // 3600  # Время в часах
            await bot.send_message(CHAT_ID, f'Бот работает уже {int(elapsed_time)} часов.')
        await asyncio.sleep(3600)  # Ожидание 1 час

# Функция для обработки текстовых сообщений
@router.message()
async def handle_message(message: types.Message):
    global messages

    # Ответы на ключевые слова
    message_text = message.text.lower()
    for keyword, response in responses.items():
        if keyword in message_text:
            await message.reply(response)
            break

    # Приветствие Ивана Владимировича
    if "доброе утро" in message_text and message.from_user.id == 786761078:
        await message.reply("Доброе утро, Иван Владимирович")

    # Реакция на флуд
    messages.append((message.chat.id, message.message_id))

    if len(messages) >= MESSAGE_THRESHOLD:
        random_message = random.choice(messages)
        chat_id, message_id = random_message
        await bot.send_message(chat_id, FRASE, reply_to_message_id=message_id)
        messages.clear()

# Функция для сброса сообщений каждые TIMEOUT секунд
async def message_reset_loop():
    global messages
    while True:
        await asyncio.sleep(TIMEOUT)
        messages.clear()

# Основная функция
async def main():
    global start_time
    start_time = asyncio.get_event_loop().time()  # Запоминаем время запуска
    await send_welcome_message()
    asyncio.create_task(message_reset_loop())  # Запускаем сброс сообщений в отдельной задаче
    asyncio.create_task(report_work_time())  # Запускаем таймер работы бота
    dp.include_router(router)  # Включаем роутер в диспетчер
    await dp.start_polling(bot)  # Запускаем обработчик событий

if __name__ == '__main__':
    asyncio.run(main())  # Запускаем основную функцию
