from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def crypto_list_pagination(current_page: int, total_pages: int, language):
    text_language_dict = {
        'eng': ['⬅️ Back', 'Next ➡️'],
        'ua': ['⬅️ Назад', 'Далі ➡️'],
        'ru': ['⬅️ Назад', 'Дальше ➡️']
    }
    buttons = []
    
    
    if current_page > 1:
        buttons.append(InlineKeyboardButton(text=text_language_dict[language][0], callback_data=f"page_{current_page - 1}"))
    
    if current_page < total_pages:
        buttons.append(InlineKeyboardButton(text=text_language_dict[language][1], callback_data=f"page_{current_page + 1}"))
    
    return InlineKeyboardMarkup(inline_keyboard=[buttons])

def market_data_button(language):
    buttons = []
    text_language_dict = {
        'eng': 'What is F&G Index ❓',
        'ua': 'Що таке F&G індекс ❓',
        'ru': 'Что такое F&G индекс ❓'
    }
    buttons.append(InlineKeyboardButton(text=text_language_dict[language], callback_data='fg_index'))
    return InlineKeyboardMarkup(inline_keyboard=[buttons])

def top_users_button(language):
    text_language_dict = {
        'eng': ['Top bot users 🔝', 'Change language 📚'],
        'ua': ['Топ користувачів боту 🔝', 'Змінити мову 📚'],
        'ru': ['Топ пользователей бота 🔝', 'Сменить язык 📚']
    }

    buttons = [
        [InlineKeyboardButton(text=text_language_dict[language][0], callback_data='top_users')],
        [InlineKeyboardButton(text=text_language_dict[language][1], callback_data='change_language')]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def language_button():
    buttons = [InlineKeyboardButton(text="English", callback_data='eng'), InlineKeyboardButton(text="Русский", callback_data='ru'), InlineKeyboardButton(text="Українська", callback_data='ua')]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])