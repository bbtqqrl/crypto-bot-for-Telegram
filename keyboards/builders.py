from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
def main_kb(language):
    items_language_dict = {
        'ua':['Список криптовалют📚', 'Пошук крипти🔎', 'Профіль📋', '📈 Стан ринку', 'Про мене!😊'],
        'eng':['List of crypto📚', 'Search crypto🔎', 'Profile📋', '📈 Market state', 'About me!😊'],
        'ru':['Список криптовалют📚', 'Поиск крипты🔎', 'Профиль📋', '📈 Состояние рынка', 'Обо мне!😊']
    }
    items = items_language_dict[language]
    builder = ReplyKeyboardBuilder()
    [builder.add(KeyboardButton(text = item)) for item in items]
    builder.adjust(2, 3)
    return builder.as_markup(resize_keyboard=True)