import psycopg2
from psycopg2.extras import RealDictCursor
import os
import uuid
import allure  # <--- Обязательно добавляем импорт


class DBClient:
    def __init__(self):
        db_url = os.getenv('SPEND_DB_URL', "postgresql://postgres:secret@localhost:5432/niffler-spend")
        db_url = db_url.replace('+psycopg2', '')

        self.conn = psycopg2.connect(db_url)
        self.conn.autocommit = True

    def get_category(self, username: str, category_name: str):
        """Получает категорию из БД по имени и юзеру"""
        query = "SELECT * FROM category WHERE username = %s AND name = %s"
        params = (username, category_name)

        with allure.step(f"DB: SELECT category '{category_name}' for user '{username}'"):
            # Прикрепляем запрос к отчету
            allure.attach(
                f"Query: {query}\nParams: {params}",
                name="SQL Query",
                attachment_type=allure.attachment_type.TEXT
            )

            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                result = cur.fetchone()

                # Прикрепляем результат (что вернула база)
                allure.attach(
                    str(result),
                    name="SQL Result",
                    attachment_type=allure.attachment_type.TEXT
                )
                return result

    def insert_category(self, username: str, category_name: str):
        """Создает категорию напрямую через SQL"""
        query = "INSERT INTO category (id, name, username, archived) VALUES (%s, %s, %s, %s)"
        params = (str(uuid.uuid4()), category_name, username, False)

        with allure.step(f"DB: INSERT category '{category_name}'"):
            allure.attach(
                f"Query: {query}\nParams: {params}",
                name="SQL Query",
                attachment_type=allure.attachment_type.TEXT
            )

            with self.conn.cursor() as cur:
                cur.execute(query, params)

    def delete_category(self, username: str, category_name: str):
        """Удаляет категорию"""
        query = "DELETE FROM category WHERE username = %s AND name = %s"
        params = (username, category_name)

        with allure.step(f"DB: DELETE category '{category_name}'"):
            allure.attach(
                f"Query: {query}\nParams: {params}",
                name="SQL Query",
                attachment_type=allure.attachment_type.TEXT
            )

            with self.conn.cursor() as cur:
                cur.execute(query, params)

    def close(self):
        self.conn.close()