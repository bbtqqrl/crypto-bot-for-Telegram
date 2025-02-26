import asyncio
import os
import threading
from flask import Flask
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from handlers import bot_message, user_commands
from callbacks import callback_handlers

# Токен бота
TOKEN = '7213514246:AAFrt2iq7MkFh-d3PKhSrjDoAok5X_1AsBc'

# Ініціалізація бота і диспетчера
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

# Функція для запуску бота у фоні
async def run_bot():
    dp.include_routers(
        user_commands.router,
        bot_message.router,
        callback_handlers.router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

def start_bot():
    asyncio.run(run_bot())

# Запуск бота у окремому потоці
threading.Thread(target=start_bot).start()

# Flask-сервер для Render
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Використовуємо порт Render
    app.run(host="0.0.0.0", port=port)
