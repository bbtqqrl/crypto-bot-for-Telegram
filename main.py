import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from flask import Flask
import threading
import os

# Ініціалізація бота 
bot = Bot('7213514246:AAFrt2iq7MkFh-d3PKhSrjDoAok5X_1AsBc', default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

# Ініціалізація Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))  # Render дає порт через змінну PORT
    app.run(host="0.0.0.0", port=port)

# Основна функція для запуску бота
async def main():
    from handlers import bot_message, user_commands
    from callbacks import callback_handlers

    dp.include_routers(
        user_commands.router,
        bot_message.router,
        callback_handlers.router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Запускаємо Flask у окремому потоці
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Запускаємо асинхронний бот
    asyncio.run(main())