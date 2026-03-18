"""Обёртка над Faker для генерации тестовых данных."""
from datetime import datetime, timedelta
import random

from faker import Faker

_faker = Faker()


class FakeDataProvider:
    """Провайдер тестовых данных, совместимый с Pydantic default_factory."""

    @staticmethod
    def text() -> str:
        return _faker.sentence(nb_words=3)

    @staticmethod
    def word() -> str:
        return _faker.word()

    @staticmethod
    def integer() -> float:
        return round(random.uniform(1, 1000), 2)

    @staticmethod
    def data() -> str:
        """Генерирует дату в формате ISO (yyyy-MM-dd)."""
        date = datetime.now() - timedelta(days=random.randint(0, 30))
        return date.strftime("%Y-%m-%d")

    @staticmethod
    def username() -> str:
        return _faker.user_name()

    @staticmethod
    def password() -> str:
        return _faker.password(length=8, special_chars=False)


fake = FakeDataProvider()

