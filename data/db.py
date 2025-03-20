import psycopg2
import os
import json
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_NAME = os.getenv("DB_NAME")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        
        if self.connection:
            self.connection.close()
        
        self.connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None, fetchone=False, fetchall=False):
        try:
            self.cursor.execute(query, params or ())
            if fetchone:
                return self.cursor.fetchone()
            if fetchall:
                return self.cursor.fetchall()
            self.connection.commit()
        except (psycopg2.OperationalError, psycopg2.InterfaceError):
            print("⚠️ Втрата з'єднання! Перепідключення...")
            self.connect()
            return self.execute_query(query, params, fetchone, fetchall)
        except Exception as e:
            print(f"Помилка: {e}")

    def insert_user(self, chat_id):
        query = "INSERT INTO users (chat_id) VALUES (%s) ON CONFLICT (chat_id) DO NOTHING"
        self.execute_query(query, (chat_id,))

    def get_language(self, chat_id):
        query = "SELECT language FROM users WHERE chat_id = %s"
        result = self.execute_query(query, (chat_id,), fetchone=True)
        return result[0] if result else None

    def update_language(self, chat_id, new_language):
        query = "UPDATE users SET language = %s WHERE chat_id = %s"
        self.execute_query(query, (new_language, chat_id))

    def update_crypto_views(self, chat_id, crypto_name):
        query = """
            INSERT INTO crypto_views (user_id, crypto_symbol, views_count)
            VALUES (%s, %s, 1)
            ON CONFLICT (user_id, crypto_symbol)
            DO UPDATE SET views_count = crypto_views.views_count + 1;
        """
        self.execute_query(query, (chat_id, crypto_name))

    def get_favorite_crypto(self, chat_id, language):
        dict_language = {
            'eng': "You don`t have favorited crypto yet 😔",
            'ua': "У тебе ще немає улюбленої крипти 😔",
            'ru': "У тебя еще нету любимой крипты 😔"
        }
        query = """
            SELECT crypto_symbol FROM crypto_views 
            WHERE user_id = %s ORDER BY views_count DESC LIMIT 1;
        """
        result = self.execute_query(query, (chat_id,), fetchone=True)
        return result[0] if result else dict_language.get(language, dict_language['eng'])

    def get_count(self, chat_id):
        query = """
            SELECT SUM(views_count) FROM crypto_views WHERE user_id = %s;
        """
        result = self.execute_query(query, (chat_id,), fetchone=True)
        return result[0] if result else 0
    
    def get_top_views(self):
        query = """
            SELECT user_id, SUM(views_count) AS total_views 
            FROM crypto_views 
            GROUP BY user_id 
            ORDER BY total_views DESC 
            LIMIT 5;
        """
        return self.execute_query(query, fetchall=True)
