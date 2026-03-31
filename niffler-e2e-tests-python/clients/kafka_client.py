"""
Kafka клиент для работы с топиком 'users'.

При регистрации нового пользователя niffler-auth публикует сообщение
в топик 'users'. Kafka-consumer позволяет:
 - проверить доставку сообщения после регистрации
 - убедиться, что userdata-сервис получил событие и создал профиль
"""
import json
import time
import allure
from typing import Optional
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError


class KafkaClient:
    """Клиент для работы с Kafka брокером."""

    TOPIC_USERS = "users"

    def __init__(self, bootstrap_servers: str):
        """
        Инициализация Kafka клиента.

        Args:
            bootstrap_servers: адрес брокера (например, 'localhost:9092')
        """
        self.bootstrap_servers = bootstrap_servers

    def consume_user_message(
            self,
            username: str,
            timeout_seconds: int = 30,
    ) -> Optional[dict]:
        """
        Читает сообщения из топика 'users' и ищет сообщение для username.

        Args:
            username: имя пользователя для поиска
            timeout_seconds: таймаут ожидания в секундах

        Returns:
            Словарь с данными сообщения или None если не найдено
        """
        consumer = KafkaConsumer(
            self.TOPIC_USERS,
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset="earliest",
            enable_auto_commit=False,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            consumer_timeout_ms=timeout_seconds * 1000,
            group_id=f"test-group-{int(time.time())}",
        )

        found_message = None
        try:
            for message in consumer:
                payload = message.value
                if isinstance(payload, dict) and payload.get("username") == username:
                    found_message = payload
                    break
                elif isinstance(payload, str) and payload == username:
                    found_message = {"username": payload}
                    break
        finally:
            consumer.close()

        return found_message

    def get_latest_messages(self, topic: str, count: int = 10) -> list:
        """
        Получает последние N сообщений из топика.

        Args:
            topic: название топика
            count: количество сообщений

        Returns:
            Список сообщений
        """
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset="latest",
            enable_auto_commit=False,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            consumer_timeout_ms=5000,
            group_id=f"test-group-latest-{int(time.time())}",
        )

        messages = []
        try:
            for message in consumer:
                messages.append(message.value)
                if len(messages) >= count:
                    break
        finally:
            consumer.close()

        return messages

    def check_topic_exists(self, topic: str) -> bool:
        """
        Проверяет существование топика.

        Args:
            topic: название топика

        Returns:
            True если топик существует
        """
        consumer = KafkaConsumer(
            bootstrap_servers=self.bootstrap_servers,
            consumer_timeout_ms=3000,
        )
        try:
            topics = consumer.topics()
            return topic in topics
        finally:
            consumer.close()

    def wait_for_user_message(
            self,
            username: str,
            timeout_seconds: int = 30,
    ) -> Optional[dict]:
        """
        Ожидает сообщение о регистрации пользователя в топике 'users'.
        Используется для проверки, что после регистрации Kafka получила событие.

        Args:
            username: имя пользователя
            timeout_seconds: таймаут ожидания

        Returns:
            Словарь с данными сообщения или None
        """
        with allure.step(f"Kafka: ожидание сообщения для пользователя '{username}'"):
            message = self.consume_user_message(username, timeout_seconds)
            if message:
                allure.attach(
                    json.dumps(message, ensure_ascii=False, indent=2),
                    name="kafka_message",
                    attachment_type=allure.attachment_type.JSON,
                )
            return message

