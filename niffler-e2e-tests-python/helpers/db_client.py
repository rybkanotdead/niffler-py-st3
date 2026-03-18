import psycopg2
from psycopg2.extras import RealDictCursor
import os
import uuid
from typing import List, Dict, Any, Optional


class DBClient:
    """Клиент для работы с БД PostgreSQL (niffler-spend)."""

    def __init__(self, db_url: str = None):
        if db_url is None:
            db_url = os.getenv('SPEND_DB_URL', "postgresql://postgres:secret@localhost:5432/niffler-spend")
        db_url = db_url.replace('+psycopg2', '')

        self.conn = psycopg2.connect(db_url)
        self.conn.autocommit = True

    # ============ КАТЕГОРИИ ============

    def get_category(self, username: str, category_name: str) -> Optional[Dict[str, Any]]:
        """Получает категорию из БД по имени и юзеру."""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM category WHERE username = %s AND name = %s",
                (username, category_name)
            )
            return cur.fetchone()

    def get_user_categories(self, username: str) -> List[Dict[str, Any]]:
        """Получает все категории пользователя."""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM category WHERE username = %s ORDER BY name",
                (username,)
            )
            return cur.fetchall()

    def insert_category(self, username: str, category_name: str) -> str:
        """
        Создает категорию напрямую через SQL.
        Возвращает ID созданной категории.
        """
        category_id = str(uuid.uuid4())
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO category (id, name, username, archived) VALUES (%s, %s, %s, %s)",
                (category_id, category_name, username, False)
            )
        return category_id

    def delete_category(self, username: str, category_name: str) -> None:
        """Удаляет категорию по имени."""
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM category WHERE username = %s AND name = %s",
                (username, category_name)
            )

    def delete_category_by_id(self, category_id: str) -> None:
        """Удаляет категорию по ID."""
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM category WHERE id = %s",
                (category_id,)
            )

    def archive_category(self, category_id: str) -> None:
        """Архивирует категорию."""
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE category SET archived = true WHERE id = %s",
                (category_id,)
            )

    # ============ ТРАТЫ ============

    def get_spend_by_id(self, spend_id: str) -> Optional[Dict[str, Any]]:
        """Получает трату по ID."""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM spend WHERE id = %s",
                (spend_id,)
            )
            return cur.fetchone()

    def get_user_spends(self, username: str) -> List[Dict[str, Any]]:
        """Получает все траты пользователя."""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT s.*, c.name as category_name 
                FROM spend s
                JOIN category c ON s.category_id = c.id
                WHERE s.username = %s
                ORDER BY s.spend_date DESC
                """,
                (username,)
            )
            return cur.fetchall()

    def insert_spend(
            self,
            username: str,
            description: str,
            amount: float,
            category_id: str,
            currency: str = "RUB"
    ) -> str:
        """
        Создает трату напрямую через SQL.
        Возвращает ID созданной траты.
        """
        spend_id = str(uuid.uuid4())
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO spend (id, username, description, amount, category_id, spend_date, currency)
                VALUES (%s, %s, %s, %s, %s, NOW(), %s)
                """,
                (spend_id, username, description, amount, category_id, currency)
            )
        return spend_id

    def delete_spend(self, spend_id: str) -> None:
        """Удаляет трату по ID."""
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM spend WHERE id = %s",
                (spend_id,)
            )

    def delete_user_spends(self, username: str) -> None:
        """Удаляет все траты пользователя."""
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM spend WHERE username = %s",
                (username,)
            )

    # ============ ОБЩИЕ ============

    def cleanup_user_data(self, username: str) -> None:
        """Удаляет все данные пользователя (траты и категории)."""
        # Сначала удаляем траты, потом категории (из-за foreign key)
        self.delete_user_spends(username)
        
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM category WHERE username = %s",
                (username,)
            )

    def close(self) -> None:
        """Закрывает подключение к БД."""
        if self.conn:
            self.conn.close()
