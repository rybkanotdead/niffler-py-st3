import psycopg2
from psycopg2.extras import RealDictCursor
import os
import uuid

class DBClient:
    def __init__(self):
        db_url = os.getenv('SPEND_DB_URL', "postgresql://postgres:secret@localhost:5432/niffler-spend")
        db_url = db_url.replace('+psycopg2', '')

        self.conn = psycopg2.connect(db_url)
        self.conn.autocommit = True

    def get_category(self, username: str, category_name: str):
        """Получает категорию из БД по имени и юзеру"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM category WHERE username = %s AND name = %s",
                (username, category_name)
            )
            return cur.fetchone()

    def insert_category(self, username: str, category_name: str):
        """Создает категорию напрямую через SQL"""
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO category (id, name, username, archived) VALUES (%s, %s, %s, %s)",
                (str(uuid.uuid4()), category_name, username, False)
            )

    def delete_category(self, username: str, category_name: str):
        """Удаляет категорию"""
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM category WHERE username = %s AND name = %s",
                (username, category_name)
            )

    def close(self):
        self.conn.close()