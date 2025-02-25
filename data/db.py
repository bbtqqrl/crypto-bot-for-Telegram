import psycopg2

class Database:
    def __init__(self):
        # Підключення до PostgreSQL
        self.connection = psycopg2.connect(
            host="dpg-cutg8cggph6c73b2fr60-a.frankfurt-postgres.render.com",
            port="5432",
            dbname="crypto_postgresql",
            user="bbtqqrl",
            password="z0VYMOLedM0GcRUKaJa48sexJuSQLVp7"
        )
        self.cursor = self.connection.cursor()

    # Додавання нового користувача по chat_id
    def insert_user(self, chat_id):
        try:
            with self.connection:
                self.cursor.execute("INSERT INTO users (chat_id) VALUES (%s)", (chat_id,))
        except Exception as e:
            print(f"Помилка при додаванні користувача: {e}")

    # Отримання count_crypto по chat_id користувача
    def get_language(self, chat_id):
        try:
            self.cursor.execute("SELECT language FROM users WHERE chat_id = %s", (chat_id,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Помилка при отриманні мови користувача: {e}")
            return None

    # Оновлення мови користувача по chat_id
    def update_language(self, chat_id, new_language):
        try:
            self.cursor.execute("UPDATE users SET language = %s WHERE chat_id = %s", (new_language, chat_id))
            self.connection.commit()
        except Exception as e:
            print(f"Помилка при оновленні мови користувача: {e}")

    def update_crypto_views(self, chat_id, crypto_name):
        try:
            self.cursor.execute("INSERT INTO crypto_views (user_id, crypto_symbol, views_count) VALUES (%s, %s, 1) ON CONFLICT (user_id, crypto_symbol) DO UPDATE SET views_count = crypto_views.views_count + 1;", (chat_id, crypto_name,))
            self.connection.commit()
        except Exception as e:
            print(f"{e}")
            return None
        
    def get_favorite_crypto(self, chat_id, language):
        dict_language = {
            'eng': 'You don`t have favorited crypto yet 😔',
            'ua': "У тебе ще немає улюбленої крипти 😔",
            'ru': 'У тебя еще нету любимой крипты 😔'
        }
        try:
            self.cursor.execute("SELECT crypto_symbol FROM crypto_views WHERE user_id = %s ORDER BY views_count DESC LIMIT 1;", (chat_id,))
            result = self.cursor.fetchone()
            return result[0] if result else dict_language[language]
        except Exception as e:
            print(f"{e}")
            return dict_language[language]
        
    def get_count(self, chat_id):
        try:
            self.cursor.execute("SELECT user_id, SUM(views_count) AS total_views FROM crypto_views WHERE user_id = %s GROUP BY user_id;", (chat_id,))
            result = self.cursor.fetchone()
            return result[1] if result else None
        except Exception as e:
            print(f"Помилка при отриманні count_crypto: {e}")
            return None
    
    def get_top_views(self):
        try:
            self.cursor.execute("SELECT user_id, SUM(views_count) AS total_views FROM crypto_views GROUP BY user_id ORDER BY total_views DESC LIMIT 5;")
            result = self.cursor.fetchall()
            return result if result else None
        except Exception as e:
            print(f"Помилка при отриманні count_crypto: {e}")
            return None 

    
