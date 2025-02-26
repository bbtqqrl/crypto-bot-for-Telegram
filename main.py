import asyncio
from aiogram import Router
from aiogram import F, Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
bot = Bot('7213514246:AAFrt2iq7MkFh-d3PKhSrjDoAok5X_1AsBc', default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()
from handlers import bot_message, user_commands
from callbacks import callback_handlers

async def main():
    dp.include_routers(
        user_commands.router,
        bot_message.router,
        callback_handlers.router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())