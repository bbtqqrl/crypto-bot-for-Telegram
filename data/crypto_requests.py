import aiohttp
from aiocache import Cache
import matplotlib.pyplot as plt
import squarify
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import io
import datetime
import matplotlib.dates as mdates
import pytz
import matplotlib.ticker as ticker
cache = Cache(Cache.MEMORY)  # Кешування у пам’яті
from . import bot_func

async def get_crypto_data(crypto_coin: str = "bitcoin"):
    data = await get_cached_data()
    if isinstance(data, list):
            for crypto in data:
                if crypto_coin.lower() in [crypto["id"].lower(), crypto["symbol"].lower(), crypto["name"].lower()]:
                    return crypto 
    else:
        return 'data is not a list'


async def get_crypto_list(page: int = 1, per_page: int = 6):
    data = await get_cached_data()
    if isinstance(data, list):
        return data[page * per_page - per_page:page * per_page]
    else:
        return 'data is not a list'


            
async def get_cached_data():
    cache_key = f"crypto_list_usd"
    cached_data = await cache.get(cache_key)
    if cached_data:
        return cached_data
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": 'usd',
        "order": "market_cap_desc",
        "per_page": 246,
        "page": 1,
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                await cache.set(cache_key, data, ttl=600)  # Кеш на 5 хвилин
                return data
            elif response.status == 404:
                return None
            elif response.status == 429:
                return 429 
            
async def get_cached_crypto(crypto_id):
    cached_data = await cache.get(crypto_id)
    if cached_data:
        return cached_data
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                await cache.set(crypto_id, data, ttl=600)  # Кеш на 10 хв
                return data
            elif response.status == 404:
                return None
            elif response.status == 429:
                return 429

async def get_cached_list():
    cached_data = await cache.get('list')
    if cached_data:
        return cached_data
    url = f"https://api.coingecko.com/api/v3/coins/list"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                await cache.set('list', data, ttl=86400)
                return data
            elif response.status == 404:
                return None
            elif response.status == 429:
                return 429
            else:
                return None

async def get_crypto_chart(crypto_id, language):
    try:
        data = await cache.get(f"chart_data_{crypto_id}")
        if not data:
            url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
            params = {
                "vs_currency": "usd",
                "days": "1",}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        await cache.set(f"chart_data_{crypto_id}", data, ttl=600)
                        
        prices = data["prices"]

        # Перетворюємо час та ціну
        times = [datetime.datetime.fromtimestamp(p[0] / 1000, tz=pytz.UTC) for p in prices]
        values = [p[1] for p in prices]
        text_language_dict = {
            'eng': ['Time', 'Price (USD)', 'Schedule ', ' for 24 hours'],
            'ua': ['Час', 'Ціна (USD)', 'Графік ', ' за 24 години'],
            'ru': ['Время', 'Цена (USD)', 'График ', ' за 24 часа']
        }
        text = text_language_dict[language]
        # Малюємо графік
        plt.figure(figsize=(6, 3))
        plt.plot(times, values, color="blue")
        plt.xlabel(text[0])
        plt.ylabel(text[1])
        plt.title(f"{text[2]} {crypto_id.upper()} {text[3]}")

        # Форматування осі X (зменшуємо шрифт і не робимо мітки по діагоналі)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=pytz.UTC))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
        plt.xticks(rotation=0, fontsize=8)  # Зменшений шрифт, без нахилу
        plt.yticks(fontsize=8)  # Зменшуємо шрифт осі Y

        plt.grid()
        ax = plt.gca()  # Отримуємо поточну вісь
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:.8f}".rstrip('0').rstrip('.')))
        img_io = io.BytesIO()
        plt.savefig(img_io, format="png", bbox_inches="tight")
        img_io.seek(0)
        plt.close()
        return img_io
    except Exception as e:
        print(e)
        return None


async def fetch_market_data():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.coingecko.com/api/v3/global") as response:
            if response.status == 200:
                data = await response.json()
                return data['data']
            return None


async def generate_crypto_heatmap(language):
    try:
        data = await get_cached_data()
        if data:
            list = data[:14]
            list = [char for char in list if char.get('symbol') not in ['usdc', 'usdt', 'wbtc', 'wsteth']]
            list = list[:10]
        else:
            return None

        crypto_data = []
        for char in list:
            crypto_data.append({
                "symbol": char.get('symbol', 'None'),
                "name": char.get('name', 'None'),
                "current_price": char.get('current_price', '0'),
                "market_cap": char.get('market_cap', '0'),
                "price_change_percentage_24h": char.get("price_change_percentage_24h", '0')
            })

        text_language_dict = {
                    'eng': ["Crypto Market Heatmap (24h)", '24h Price Change (%)'],
                    'ua': ["Теплова карта крипторинку (24h)", "Зміна ціни (%)"],
                    'ru': ["Тепловая карта крипторынка (24h)", "Изменение цены (%)"]
                }
        text = text_language_dict[language]

        sorted_data = sorted(crypto_data, key=lambda x: x['market_cap'], reverse=True)
        
        sizes = [np.sqrt(d['market_cap']) for d in sorted_data]
        labels = [f"{d['symbol'].upper()}\n${d['current_price']:,.2f}\n{d['price_change_percentage_24h']:.2f}%" for d in sorted_data]
        price_changes = [d['price_change_percentage_24h'] for d in sorted_data]

        # Покращена колірна схема
        cmap = LinearSegmentedColormap.from_list("custom", ["#8B0000", "#FFFFFF", "#006400"])

        norm = plt.Normalize(vmin=-6, vmax=6)
        colors = cmap(norm(price_changes))

        # **Формат для телефону (портретна орієнтація)**
        fig, ax = plt.subplots(figsize=(11, 7))

        # Додаємо обводку для блоків
        squarify.plot(
            sizes=sizes, label=labels, color=colors, alpha=0.85,
            text_kwargs={'fontsize': 12, 'fontweight': 'bold', 'color': "black"},
            ax=ax, edgecolor="white", linewidth=2
        )

        ax.axis('off')
        ax.set_title(text[0], fontsize=22, fontweight="bold", pad=20)

        # Колірна шкала
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, orientation="vertical", fraction=0.04, pad=0.05)
        cbar.set_label(text[1], rotation=270, labelpad=20, fontsize=14, fontweight="bold")

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)
        return buf
    except Exception as e:
        print(e)
        return None
    
async def get_market_summary(language):
    try:
        cached_data = await cache.get(f"market_summary")
        if cached_data:
            market_data = cached_data[0]
            fng_data = cached_data[1]
        else:
            async with aiohttp.ClientSession() as session:
                url_market = f"https://api.cryptorank.io/v1/global?api_key=ec13a60cf2c668b8e6fd2e40ef9f1c81d78082b7ab5b6d01e2d31c90fe2b"
                async with session.get(url_market) as response:
                    market_data = await response.json()
                url_fng = "https://api.alternative.me/fng/"
                async with session.get(url_fng) as response:
                    fng_data = await response.json()
                await cache.set(f"market_summary", [market_data, fng_data], ttl=600)
        text_language_dict = {
            'eng': ['🔴 RED', '🟢 GREEN', '⚪️ NEUTRAL'],
            'ua': ['🔴 ЧЕРВОНИЙ', '🟢 ЗЕЛЕНИЙ', '⚪️ НЕЙТРАЛЬНИЙ'],
            'ru': ['🔴 КРАСНЫЙ', '🟢 ЗЕЛЕНЫЙ', '⚪️ НЕЙТРАЛЬНЫЙ']
        }
        text = text_language_dict[language]
        prices_data = await get_cached_data()
        prices_data = prices_data[:2]
        change_percentage = float(prices_data[0]['price_change_percentage_24h']) + float(prices_data[1]['price_change_percentage_24h'])
        list = [
            prices_data[0].get('current_price'),
            prices_data[1].get('current_price'),
            market_data["data"]["values"]["USD"]["totalMarketCap"],
            market_data["data"]["btcDominance"],
            fng_data["data"][0]["value"],
            fng_data["data"][0]["value_classification"],
            text[0] if change_percentage < -0.5 else text[1] if change_percentage > 0.5 else text[2]
        ]
        return list
    except Exception as e:
        print(e)
        return 'Error get data , try again later'