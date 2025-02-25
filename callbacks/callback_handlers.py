from aiogram import Router, F
from aiogram.types import CallbackQuery
from data import crypto_requests
from keyboards import inline, builders
from datetime import datetime
from data.db import Database
db = Database()
router = Router()

@router.callback_query(lambda c: c.data.startswith("page_"))
async def handle_pagination(callback_query: CallbackQuery):
    try:
        _, current_page = callback_query.data.split("_")
        current_page = int(current_page)
        language = db.get_language(callback_query.message.chat.id)

        # Отримуємо нову сторінку криптовалют
        cryptos = await crypto_requests.get_crypto_list(page=current_page, per_page=6)

        # Формуємо повідомлення з новими криптовалютами
        text = ''
        for crypto in cryptos:
            name = crypto.get("name")
            symbol = crypto.get("symbol")
            price = crypto.get("current_price")
            market_cap = crypto.get("market_cap")
            text_language_dict = {'ua': '📊 Капіталізація', 'ru': '📊 Капитализация', 'eng': '📊 Capitalization'}
            text += f"<b>{name}</b> (<code>{symbol.upper()}</code>) - <b>{price}</b> USD\n{text_language_dict[language]}: {market_cap:,} USD\n\n"

        # Створюємо нову пагінацію
        pagination_buttons = inline.crypto_list_pagination(current_page, 41, language)  # 10 - загальна кількість сторінок (можеш змінити)

        # Оновлюємо повідомлення з новими криптовалютами та кнопками пагінації
        await callback_query.message.edit_text(text, reply_markup=pagination_buttons)

        # Підтверджуємо обробку callback-запиту
        await callback_query.answer()
    
    except Exception as e:
        print(e)
        await callback_query.answer("❌ Error processing request.")

@router.callback_query(F.data == 'fg_index')
async def fg_handler(callback_query: CallbackQuery):
    today = datetime.today()
    today = today.strftime("%Y-%m-%d")
    today = "-".join([char.lstrip('0') for char in today.split('-')])
    image = f"https://alternative.me/images/fng/crypto-fear-and-greed-index-{today}.png"
    text_language_dict = {'eng': f'<b>What is the Fear and Greed Index in Crypto?</b>\n\nSimilar to traditional markets, cryptocurrencies have their own unique Fear and Greed Index, commonly known as the Crypto Fear and Greed Index. This index gathers information from various online sources to get a good idea of public sentiment towards the crypto giant Bitcoin and other altcoins.\n\nThe Crypto Fear and Greed Index assesses several key factors. It analyzes the price fluctuations over the previous month plus the last three months, observes trading activity, and notes the pace of price changes. Additionally, it monitors social media platforms like Twitter and goes through hashtags related to different cryptocurrencies to get an idea of public consensus. The index also evaluates Bitcoin’s dominance among other cryptocurrencies and tracks online search volumes for Bitcoin. All these factors converge to provide a snapshot of how people perceive the crypto market at that time.',
                          'ua': f"<b>Що таке Індекс страху та жадібності у криптовалюті?</b>\n\nПодібно до традиційних ринків, криптовалюти мають свій власний унікальний Індекс страху та жадібності, який зазвичай називають Crypto Fear and Greed Index. Цей індекс збирає інформацію з різних онлайн-джерел, щоб зрозуміти громадські настрої щодо криптовалютного гіганта Bitcoin та інших альткоїнів.\n\nCrypto Fear and Greed Index оцінює кілька ключових факторів. Він аналізує коливання цін за попередній місяць, а також за останні три місяці, спостерігає за торговою активністю та відстежує темп зміни цін. Крім того, він моніторить соціальні мережі, такі як Twitter, аналізуючи хештеги, пов’язані з різними криптовалютами, щоб отримати загальну картину суспільної думки. Індекс також оцінює домінування Bitcoin серед інших криптовалют та відстежує онлайн-пошукові запити, пов’язані з Bitcoin. Усі ці фактори разом дають загальне уявлення про те, як люди сприймають ринок криптовалют у цей момент.",
                          'ru': f"<b>Что такое Индекс страха и жадности в криптовалюте?</b>\n\nПодобно традиционным рынкам, криптовалюты имеют свой собственный уникальный Индекс страха и жадности, который обычно называют Crypto Fear and Greed Index. Этот индекс собирает информацию из различных онлайн-источников, чтобы получить представление об общественном настроении по отношению к криптовалютному гиганту Bitcoin и другим альткоинам.\n\nCrypto Fear and Greed Index оценивает несколько ключевых факторов. Он анализирует колебания цен за предыдущий месяц, а также за последние три месяца, наблюдает за торговой активностью и отслеживает скорость изменения цен. Кроме того, он мониторит социальные сети, такие как Twitter, анализируя хэштеги, связанные с разными криптовалютами, чтобы получить представление об общественном мнении. Индекс также оценивает доминирование Bitcoin среди других криптовалют и отслеживает объем поисковых запросов по Bitcoin. Все эти факторы вместе дают представление о том, как люди воспринимают рынок криптовалют в данный момент."}
    await callback_query.message.reply_photo(image, text_language_dict[db.get_language(callback_query.message.chat.id)])
    await callback_query.answer()


@router.callback_query(F.data == 'top_users')
async def top_users(callback_query: CallbackQuery):
    users = db.get_top_views()
    users = [[users[i][0], users[i][1]] if i < len(users) else [None, None] for i in range(5)]

    text_language_dict = {
        'eng' : (f'<b>Top bot users by viewing cryptocurrencies👀⤵️</b>\n\n'
            f'<b>🥇 ID : {users[0][0]} , Views : {users[0][1]}</b>\n'
            f'<b>🥈 ID : {users[1][0]} , Views : {users[1][1]}</b>\n'
            f'<b>🥉 ID : {users[2][0]} , Views : {users[2][1]}</b>\n'
            f'<b>4 ID : {users[3][0]} , Views : {users[3][1]}</b>\n'
            f'<b>5 ID : {users[4][0]} , Views : {users[4][1]}</b>\n\n'
            f'<b>Thanks for your activity! 💋</b>'),
        'ua' : (f'<b>Топ юзерів бота по перегляду крипти👀⤵️</b>\n\n'
            f'<b>🥇 ID : {users[0][0]} , Переглядів : {users[0][1]}</b>\n'
            f'<b>🥈 ID : {users[1][0]} , Переглядів : {users[1][1]}</b>\n'
            f'<b>🥉 ID : {users[2][0]} , Переглядів : {users[2][1]}</b>\n'
            f'<b>4 ID : {users[3][0]} , Переглядів : {users[3][1]}</b>\n'
            f'<b>5 ID : {users[4][0]} , Переглядів : {users[4][1]}</b>\n\n'
            f'<b>Дякую за вашу активність! 💋</b>'),
        'ru' : (f'<b>Топ юзеров бота по просмотру криптовалют👀⤵️</b>\n\n'
            f'<b>🥇 ID : {users[0][0]} , Просмотров : {users[0][1]}</b>\n'
            f'<b>🥈 ID : {users[1][0]} , Просмотров : {users[1][1]}</b>\n'
            f'<b>🥉 ID : {users[2][0]} , Просмотров : {users[2][1]}</b>\n'
            f'<b>4 ID : {users[3][0]} , Просмотров : {users[3][1]}</b>\n'
            f'<b>5 ID : {users[4][0]} , Просмотров : {users[4][1]}</b>\n\n'
            f'<b>Спасибо за вашу активность! 💋</b>')

    }
    users = db.get_top_views()
    await callback_query.message.answer(text_language_dict[db.get_language(callback_query.message.chat.id)])

@router.callback_query(F.data.in_(['ua', 'eng', 'ru']))
async def language_func(callback_query: CallbackQuery):
    text_language_dict = {'ua': '✅ Супер! Тепер усе працює українською. Гайда тестувати бота! 🚀',
                          'eng': '✅ Awesome! The bot is now in English. Let’s get started! 🚀',
                          'ru': '✅ Отлично! Теперь бот на русском. Вперёд к делу! 🚀'}
    db.update_language(callback_query.message.chat.id, callback_query.data)
    await callback_query.message.delete()
    await callback_query.message.answer(text_language_dict[callback_query.data], reply_markup=builders.main_kb(callback_query.data))

@router.callback_query(F.data == 'change_language')
async def change_language(callback_query: CallbackQuery):
    text_language_dict = {'eng': f"Choose a new language 📚⤵️",
                          'ua': f"Виберіть нову мову 📚⤵️",
                          'ru': f"Выберите новый язык 📚⤵️"}
    await callback_query.message.answer(text_language_dict[db.get_language(callback_query.message.chat.id)], reply_markup=inline.language_button())
    await callback_query.answer()