import asyncio
from aiogram import Router
from aiogram import F, Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboards import inline, builders
from data.db import Database
router = Router()
db = Database()
@router.message(CommandStart())
async def command(message: Message):
    language = db.get_language(message.chat.id)
    if not language:
        db.insert_user(message.chat.id)
        await message.answer('<b>Hi! 👋 \n\n I\'m a cryptocurrency tracking bot</b>\n\n↓ Choose your language ↓', reply_markup= inline.language_button())
    elif language in ['ua', 'eng', 'ru']:
        text_language_dict = {
            'ua': f'<b>Привіт </b>{message.from_user.first_name} !\n<b>Я бот для відстеження криптовалют і крипторинку</b>\n\n↓ Меню ↓',
            'ru': f'<b>Привет </b>{message.from_user.first_name} !\n<b>Я бот для отслеживания криптовалют и крипторынка</b>\n\n↓ Меню ↓',
            'eng': f'<b>Hi </b>{message.from_user.first_name} !\n<b>I\'m a cryptocurrency tracking bot and crypto market</b>\n\n↓ Menu ↓'
        }
        await message.answer(text_language_dict[language], reply_markup= builders.main_kb(language))
