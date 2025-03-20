import aiohttp
from io import BytesIO
from PIL import Image
import tempfile
from . import db
db = db.Database()

async def get_crypto_logo_sticker(logo_url):
    """ Завантажує лого крипти та конвертує його у стікер """
    async with aiohttp.ClientSession() as session:
        async with session.get(logo_url) as resp:
            if resp.status == 200:
                img_data = await resp.read()
                img_io = BytesIO(img_data)
                
                # Конвертуємо в WEBP
                img = Image.open(img_io).convert("RGBA")

                # Створюємо тимчасовий файл
                with tempfile.NamedTemporaryFile(delete=False, suffix=".webp") as temp_file:
                    img.save(temp_file, format="WEBP", quality=100)
                    return temp_file.name  # Повертаємо шлях до файлу

    return None

def convert_to_normal(num):
    return f"{num:.10f}".rstrip('0').rstrip('.')  # Відкидаємо зайві нулі


def get_text(data, language):
    name = data.get('name')
    id = data.get('id')
    symbol = data.get('symbol')
    if symbol:
        symbol = symbol.upper()
    
    price = data.get('market_data').get('current_price').get('usd')
    if price:
        price = convert_to_normal(price)
    market_cap = data.get('market_data').get('market_cap').get('usd')
    high_24h = data.get('market_data').get('high_24h').get('usd')
    low_24h = data.get('market_data').get('low_24h').get('usd')
    change_percentage_24h = data.get('market_data').get('price_change_percentage_24h')
    ath = data.get('market_data').get('ath_date').get('usd')
    ath_date = None
    if ath:
        ath_date = ath[:10]
    atl = data.get('market_data').get('atl_date').get('usd')
    atl_date = None
    if atl:
        atl_date = atl[:10]
    total_volume = data.get('market_data').get('total_volume').get('usd')
    circulating_supply = data.get('market_data').get('circulating_supply')
    date = data.get('last_updated')
    if date:
        date = date.split('T')
        date = str(date[0]) +'' + str(date[1][0:8] +'' + 'UTC +2')
    return [text_language_dict[language], name]
    

def get_cache_text(data, language):
    name = data.get('name')
    id = data.get('id')
    symbol = data.get('symbol')
    if symbol:
        symbol = symbol.upper()
    
    price = data.get('current_price')
    if price:
        price = convert_to_normal(price)
    market_cap = data.get('market_cap')
    high_24h = data.get('high_24h')
    low_24h = data.get('low_24h')
    change_percentage_24h = data.get('price_change_percentage_24h')
    ath = data.get('ath_date')
    ath_date = None
    if ath:
        ath_date = ath[:10]
    atl = data.get('atl_date')
    atl_date = None
    if atl:
        atl_date = atl[:10]
    total_volume = data.get('total_volume')
    circulating_supply = data.get('circulating_supply')
    date = data.get('last_updated')
    if date:
        date = date.split('T')
        date = str(date[0]) +'' + str(date[1][0:8] +'' + 'UTC +2')
    return [text_language_dict[language], name]


def find_crypto(crypto_list, target):
    crypto_dict = {item[key].lower(): item['id'] for item in crypto_list for key in ['id', 'symbol', 'name']}
    return crypto_dict.get(target.lower().strip(), None)


text_language_dict = {
    'ua' : (f"📌 <b>{name}</b> (<code>{symbol}</code>)\n\n"
            f"💰 <b>Ціна:</b> {price} USD\n"
            f"📊 <b>Ринкова капіталізація:</b> {market_cap} USD\n\n"
            f"📈 <b>Максимальна ціна за 24 години:</b> {high_24h} USD\n"
            f"📉 <b>Мінімальна ціна за 24 години:</b> {low_24h} USD\n"
            f"🔄 <b>Зміна за 24 години:</b> {change_percentage_24h}%\n\n"
            f"📅 <b>Дата ATH:</b> {ath_date} ({ath} USD)\n"
            f"📉 <b>Дата ATL:</b> {atl_date} ({atl} USD)\n\n"
            f"🔄 <b>Загальний обсяг торгів:</b> {total_volume} USD\n"
            f"🔄 <b>Кількість в обігу:</b> {circulating_supply} {symbol}\n"
            f"📅 <b>Останнє оновлення:</b> {date}\n"),
    'eng' : (f"📌 <b>{name}</b> (<code>{symbol}</code>)\n\n"
            f"💰 <b>Price:</b> {price} USD\n"
            f"📊 <b>Market Capitalization:</b> {market_cap} USD\n\n"
            f"📈 <b>24h High:</b> {high_24h} USD\n"
            f"📉 <b>24h Low:</b> {low_24h} USD\n"
            f"🔄 <b>24h Change:</b> {change_percentage_24h}%\n\n"
            f"📅 <b>ATH Date:</b> {ath_date} ({ath} USD)\n"
            f"📉 <b>ATL Date:</b> {atl_date} ({atl} USD)\n\n"
            f"🔄 <b>Total Trading Volume:</b> {total_volume} USD\n"
            f"🔄 <b>Circulating Supply:</b> {circulating_supply} {symbol}\n"
            f"📅 <b>Last Update:</b> {date}\n"),
    'ru'  : (f"📌 <b>{name}</b> (<code>{symbol}</code>)\n\n"
            f"💰 <b>Цена:</b> {price} USD\n"
            f"📊 <b>Рыночная капитализация:</b> {market_cap} USD\n\n"
            f"📈 <b>Максимальная цена за 24 часа:</b> {high_24h} USD\n"
            f"📉 <b>Минимальная цена за 24 часа:</b> {low_24h} USD\n"
            f"🔄 <b>Изменение за 24 часа:</b> {change_percentage_24h}%\n\n"
            f"📅 <b>Дата ATH:</b> {ath_date} ({ath} USD)\n"
            f"📉 <b>Дата ATL:</b> {atl_date} ({atl} USD)\n\n"
            f"🔄 <b>Общий объем торгов:</b> {total_volume} USD\n"
            f"🔄 <b>Количество в обращении:</b> {circulating_supply} {symbol}\n"
            f"📅 <b>Последнее обновление:</b> {date}\n")
}
