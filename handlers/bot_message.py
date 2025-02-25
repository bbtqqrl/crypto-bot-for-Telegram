from aiogram import Router
from aiogram import F, Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from keyboards import inline
from aiogram.types import BufferedInputFile
from data import crypto_requests
from data import bot_func
from keyboards import builders
from main import bot
import asyncio
import os
router = Router()
from data.db import Database
db = Database()


@router.message(F.text == 'bbtqqrl_send_message')
async def market_status(message: Message):
    if int(message.chat.id) == 1135699139:
        while True:
            await bot.send_message(message.chat.id, 'green')
            await asyncio.sleep(600)

@router.message(F.text.in_(["📈 Market state", '📈 Состояние рынка', '📈 Стан ринку']))
async def market_status(message: Message):
    language = db.get_language(message.chat.id)
    image = await crypto_requests.generate_crypto_heatmap(language)
    if image:
        list = await crypto_requests.get_market_summary(language)
        if len(list) == 7:
            text_language_dict = {
                'ua':  
                    f"📊Що по риночку?\n\n"
                    f"Риночок сьогодні {list[6]}, BTC торгується ±${list[0]:,.0f}, ETH ±${list[1]:,.0f}.\n\n"
                    f"Індекс страху і жадібності: {list[4]} ({list[5].lower()});\n"
                    f"Капіталізація ринку: ${list[2]/1e12:.2f} трлн.\n"
                    f"Домінація BTC: {list[3]:.1f}%",
                
                'eng':  
                    f"📊Market Update\n\n"
                    f"The market is {list[6]} today, BTC is trading at ±${list[0]:,.0f}, ETH at ±${list[1]:,.0f}.\n\n"
                    f"Fear & Greed Index: {list[4]} ({list[5].lower()});\n"
                    f"Market capitalization: ${list[2]/1e12:.2f}T.\n"
                    f"BTC dominance: {list[3]:.1f}%",
                
                'ru':  
                    f"📊Что на рынке?\n\n"
                    f"Сегодня рынок {list[6]}, BTC торгуется ±${list[0]:,.0f}, ETH ±${list[1]:,.0f}.\n\n"
                    f"Индекс страха и жадности: {list[4]} ({list[5].lower()});\n"
                    f"Рыночная капитализация: ${list[2]/1e12:.2f} трлн.\n"
                    f"Доминация BTC: {list[3]:.1f}%"}
            image_bytes = image.getvalue()
            input_file = BufferedInputFile(image_bytes, filename="chart.png")
            button = inline.market_data_button(language)
            await message.answer_photo(photo=input_file, caption=text_language_dict[language], reply_markup=button)
        else:
            await message.answer('Error getting market summary.\n\nTry again later.')


@router.message(F.text.in_(["About me!😊", "Про мене!😊", "Обо мне!😊"]))
async def market_status(message: Message):
    text_language_dict = {
        'ua': (
            f"<b>Про мене!</b>\n\n"
            f"Привіт! Я <b>Максим Горельчик</b>, 18-річний Python-розробник, який захоплюється створенням розумних і ефективних рішень. Я <b>люблю</b> вирішувати складні завдання, оптимізувати процеси та постійно вдосконалювати свої навички.\n\n"
            f"Я <b>відкритий</b> до нових ідей та можливостей, будь то цікавий проєкт, співпраця чи фріланс. Якщо у вас є щось цікаве—<b>зв’яжіться зі мною!</b> 🚀\n\n"
            f"Цей бот побудований на async <code><b>Python</b></code> і <code><b>Aiogram</b></code>, інтегрує <code><b>PostgreSQL</b></code> та отримує ринкові дані в реальному часі за допомогою різних <code><b>API</b></code>. Це лише один із багатьох проєктів у моєму портфоліо.\n\n"
            f"🔗 <a href='https://github.com/bbtqqrl'><b>GitHub</b></a>\n"
            f"🔗 <a href='https://www.linkedin.com/in/bbtqqrl/'><b>LinkedIn</b></a>"
        ),
        'eng': (
            f"<b>About Me!</b>\n\n"
            f"Hi! I’m <b>Maksym Horelchyk</b>, an 18-year-old Python developer passionate about creating smart and efficient solutions. I <b>enjoy</b> tackling complex problems, optimizing processes, and continuously improving my skills.\n\n"
            f"I’m <b>always open</b> to new ideas and opportunities, whether it’s an interesting project, collaboration, or freelance work. If you have something exciting in mind—<b>let’s connect!</b> 🚀\n\n"
            f"This bot is built with async <code><b>Python</b></code> and <code><b>Aiogram</b></code>, integrates <code><b>PostgreSQL</b></code>, and fetches real-time market data using various <code><b>APIs</b></code>. It’s just one of many projects in my growing portfolio.\n\n"
            f"🔗 <a href='https://github.com/bbtqqrl'><b>GitHub</b></a>\n"
            f"🔗 <a href='https://www.linkedin.com/in/bbtqqrl/'><b>LinkedIn</b></a>"
        ),
        'ru': (
            f"<b>Обо мне!</b>\n\n"
            f"Привет! Я <b>Максим Горельчик</b>, 18-летний Python-разработчик, увлечённый созданием умных и эффективных решений. Я <b>люблю</b> решать сложные задачи, оптимизировать процессы и постоянно совершенствовать свои навыки.\n\n"
            f"Я <b>открыт</b> для новых идей и возможностей, будь то интересный проект, сотрудничество или фриланс. Если у вас есть что-то интересное—<b>свяжитесь со мной!</b> 🚀\n\n"
            f"Этот бот построен на async <code><b>Python</b></code> и <code><b>Aiogram</b></code>, интегрирует <code><b>PostgreSQL</b></code> и получает рыночные данные в реальном времени с помощью различных <code><b>API</b></code>. Это всего лишь один из многих проектов в моем портфолио.\n\n"
            f"🔗 <a href='https://github.com/bbtqqrl'><b>GitHub</b></a>\n"
            f"🔗 <a href='https://www.linkedin.com/in/bbtqqrl/'><b>LinkedIn</b></a>"
        )
    }

    await message.answer(text_language_dict[db.get_language(message.chat.id)])

@router.message(F.text.in_(["Profile📋", "Профиль📋", "Профіль📋"]))
async def market_status(message: Message):
    language = db.get_language(message.chat.id)
    text_language_dict = {
        'eng': (
            f"<b>📋 Your Profile </b>\n\n"
            f"<b>🆔 : <code>{message.chat.id}</code></b>\n"
            f"<b>🤖 Nickname</b> : {message.from_user.first_name}\n"
            f"<b>📚 Language</b> : {db.get_language(message.chat.id)}\n\n"
            f"<b>👀 Crypto views</b> : {db.get_count(message.chat.id)}\n\n"
            f"<b>🏆 Your favorite crypto</b> : {db.get_favorite_crypto(message.chat.id, language)}\n\n"
        ),

        'ua': (
            f"<b>📋 Твій профіль </b>\n\n"
            f"<b>🆔 : <code>{message.chat.id}</code></b>\n"
            f"<b>🤖 Нікнейм</b> : {message.from_user.first_name}\n"
            f"<b>📚 Мова</b> : {db.get_language(message.chat.id)}\n\n"
            f"<b>👀 Перегляди крипти</b> : {db.get_count(message.chat.id)}\n\n"
            f"<b>🏆 Твоя улюблена крипта</b> : {db.get_favorite_crypto(message.chat.id, language)}\n\n"
        ),

        'ru': (
            f"<b>📋 Твой профиль </b>\n\n"
            f"<b>🆔 : <code>{message.chat.id}</code></b>\n"
            f"<b>🤖 Никнейм</b> : {message.from_user.first_name}\n"
            f"<b>📚 Язык</b> : {db.get_language(message.chat.id)}\n\n"
            f"<b>👀 Просмотры крипты</b> : {db.get_count(message.chat.id)}\n\n"
            f"<b>🏆 Твоя любимая крипта</b> : {db.get_favorite_crypto(message.chat.id, language)}\n\n"
        )
    }
    await message.answer(text_language_dict[language], reply_markup=inline.top_users_button(language))



# Функція для отримання курсу криптовалют
@router.message(F.text.in_(['List of crypto📚', 'Список криптовалют📚']))
async def top_cryptos(message: Message):
    current_page = 1
    cryptos = await crypto_requests.get_crypto_list(page=1, per_page=6)
    language = db.get_language(message.chat.id)
    try:
        if isinstance(cryptos, list):
            text = ''
            for crypto in cryptos:
                name = crypto.get("name")
                symbol = crypto.get("symbol")
                price = crypto.get("current_price")
                market_cap = crypto.get("market_cap")
                text_language_dict = {'ua': '📊 Капіталізація', 'ru': '📊 Капитализация', 'eng': '📊 Capitalization'}
                text += f"<b>{name}</b> (<code>{symbol.upper()}</code>) - <b>{price}</b> USD\n{text_language_dict[language]}: {market_cap:,} USD\n\n"
                pagination_buttons = inline.crypto_list_pagination(current_page, 41, language)
            
            await message.answer(text, reply_markup= pagination_buttons)
        else:
            await message.answer(cryptos)
    except Exception as e:
        print(e)
        await message.answer("❌ Error processing request.")

@router.message(F.text.in_(['Search crypto🔎', 'Поиск крипты🔎', 'Пошук крипти🔎']))
async def top_cryptos(message: Message):
    language = db.get_language(message.chat.id)
    search_prompt_language_dict = {
        'ua': (
            f"🔎 <b>Шукаєте криптовалюту?</b>\n\n"
            f"Просто введіть її назву або тікер у чат, і я знайду її для вас! \n\n"
            f"💡 <b>Ви можете ввести повну назву, наприклад, <code>Bitcoin</code>, або просто тікер <code>BTC</code></b>.\n\n"
            f"👇 <i>Спробуйте прямо зараз!</i>"
        ),
        'eng': (
            f"🔎 <b>Looking for a cryptocurrency?</b>\n\n"
            f"Just type its name or ticker symbol in the chat, and I’ll find it for you! \n\n"
            f"💡 <b>You can enter the full name like <code>Bitcoin</code> or just the ticker <code>BTC</code></b>.\n\n"
            f"👇 <i>Try it now!</i>"
        ),
        'ru': (
            f"🔎 <b>Ищете криптовалюту?</b>\n\n"
            f"Просто введите её название или тикер в чат, и я найду её для вас! \n\n"
            f"💡 <b>Вы можете ввести полное название, например, <code>Bitcoin</code>, или просто тикер <code>BTC</code></b>.\n\n"
            f"👇 <i>Попробуйте прямо сейчас!</i>")}
    await message.answer(search_prompt_language_dict[language])
    

@router.message()
async def handle_crypto_request(message: Message):
    await crypto_requests.get_cached_list()
    language = db.get_language(message.chat.id)
    text_language_dict_429 = {
        'ua':  "Занадто багато запитів . Спробуйте ще раз пізніше",
        'eng':  "Too many requests. Please try again later.",
        'ru': "Слишко много запросов . Попробуйте еще раз позже"
    }
    text_language_dict_404 = {
        'ua':  "Нажаль ми не змогли знайти криптовалюту з таким іменем . Спробуйте ще раз",
        'eng':  "Unfortunately, we couldn't find a cryptocurrency with that name. Please try again.",
        'ru': "К сожалению мы не смогли найти криптовалюту с таким именем . Попробуйте еще раз"
    }
    crypto_data = await crypto_requests.get_crypto_data(message.text)
    if crypto_data == 429:
        await message.answer(text_language_dict_429[language])


    elif crypto_data:
        data = bot_func.get_cache_text(crypto_data, language)
        text = data[0]
        crypto_name = data[1]
        img = await crypto_requests.get_crypto_chart(crypto_data.get('id'), language)
        if img != 429 and img is not None:
            img_bytes = img.getvalue()
            input_file = BufferedInputFile(img_bytes, filename="chart.png")
            await message.answer_photo(input_file, caption=text, reply_markup=builders.main_kb(language))
        else:
            await message.answer(text)
        logo_sticker = await bot_func.get_crypto_logo_sticker(crypto_data.get('image'))
        if logo_sticker:
            await message.answer_sticker(FSInputFile(logo_sticker))
            os.remove(logo_sticker)
        db.update_crypto_views(message.chat.id, crypto_name)
        
    else:
        crypto_list = await crypto_requests.get_cached_list()
        if crypto_list == 429:
            await message.answer(text_language_dict_429[language])
        elif crypto_list != None:
            crypto_coin = bot_func.find_crypto(crypto_list, message.text)

            if crypto_coin == None:
                await message.answer(text_language_dict_404[language])
            elif crypto_coin:
                not_list_crypto_data = await crypto_requests.get_cached_crypto(crypto_coin)
                if not_list_crypto_data == 429:
                    await message.answer(text_language_dict_429[language])
                elif not_list_crypto_data:
                    data = bot_func.get_text(not_list_crypto_data, language)
                    text = data[0]
                    crypto_name = data[1]
                    img = await crypto_requests.get_crypto_chart(not_list_crypto_data.get('id'), language)
                    if img != 429 and img is not None:
                        img_bytes = img.getvalue()
                        
                        input_file = BufferedInputFile(img_bytes, filename="chart.png")

                        await message.answer_photo(input_file, caption=text, reply_markup=builders.main_kb(language))
                    else:
                        await message.answer(text)
                    logo_sticker = await bot_func.get_crypto_logo_sticker(not_list_crypto_data.get("image").get("large"))
                    if logo_sticker:
                        await message.answer_sticker(FSInputFile(logo_sticker), reply_markup=builders.main_kb(language))
                        os.remove(logo_sticker)
                    db.update_crypto_views(message.chat.id, crypto_name)
                else:
                    await message.answer(text_language_dict_404[language])

