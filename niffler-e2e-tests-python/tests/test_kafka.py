"""
Kafka тесты для Niffler.

Тесты проверяют:
1. Существование топика 'users' в Kafka
2. Публикацию события регистрации пользователя в Kafka
3. Корректность структуры Kafka сообщения

Принцип работы:
- При регистрации нового пользователя niffler-auth публикует
  сообщение {"username": "..."} в топик 'users'
- niffler-userdata подписывается на этот топик и создаёт профиль
"""
import pytest
import allure
from faker import Faker

from clients.kafka_client import KafkaClient
from pages.auth_reg_page import AuthRegistrationPage

faker = Faker()


@pytest.mark.kafka
@pytest.mark.smoke
class TestKafkaTopics:
    """Тесты проверки работы Kafka."""

    @allure.title("Kafka: топик 'users' существует")
    @allure.description(
        """
        Шаги:
        1. Подключаемся к Kafka брокеру
        2. Запрашиваем список топиков
        3. Проверяем наличие топика 'users'

        Ожидается: топик 'users' существует в Kafka
        """
    )
    @allure.feature("Kafka")
    @allure.story("Topics")
    def test_users_topic_exists(self, kafka_client: KafkaClient):
        """Проверка существования топика 'users'."""
        with allure.step("Проверка существования топика 'users'"):
            exists = kafka_client.check_topic_exists(KafkaClient.TOPIC_USERS)
            assert exists, f"Топик '{KafkaClient.TOPIC_USERS}' должен существовать в Kafka"


@pytest.mark.kafka
@pytest.mark.integration
class TestKafkaRegistration:
    """Тесты проверки Kafka событий при регистрации."""

    @allure.title("Kafka: регистрация пользователя публикует событие в топик 'users'")
    @allure.description(
        """
        Предусловие: Kafka брокер доступен

        Шаги:
        1. Регистрируем нового пользователя через UI
        2. Ожидаем появления сообщения в топике 'users'
        3. Проверяем, что сообщение содержит корректный username

        Ожидается: в топике 'users' появилось сообщение о новом пользователе
        """
    )
    @allure.feature("Kafka")
    @allure.story("Registration event")
    @pytest.mark.skip(reason="Kafka может быть медленной или недоступной в локальной среде")
    def test_registration_publishes_kafka_event(
            self,
            auth_page: AuthRegistrationPage,
            kafka_client: KafkaClient,
            generate_user_data: dict,
    ):
        """
        Регистрация пользователя через UI должна опубликовать событие в Kafka.
        """
        new_user = generate_user_data
        username = new_user["username"]
        password = new_user["password"]

        with allure.step(f"Регистрация нового пользователя '{username}'"):
            auth_page.open_auth_page()
            auth_page.go_to_register_page()
            auth_page.fill_register_form(
                username=username,
                password=password,
                submit_password=password,
            )
            auth_page.submit_register_form()

        with allure.step(f"Ожидание Kafka события для '{username}'"):
            message = kafka_client.wait_for_user_message(username, timeout_seconds=60)

        with allure.step("Проверка Kafka сообщения"):
            assert message is not None, (
                f"Kafka сообщение для пользователя '{username}' не получено за 60 секунд"
            )
            assert message.get("username") == username, (
                f"Username в Kafka сообщении не совпадает: "
                f"ожидалось '{username}', получено '{message.get('username')}'"
            )

    @allure.title("Kafka: структура сообщения о регистрации корректна")
    @allure.description(
        """
        Шаги:
        1. Читаем последние сообщения из топика 'users'
        2. Проверяем структуру каждого сообщения

        Ожидается: каждое сообщение содержит поле 'username'
        """
    )
    @allure.feature("Kafka")
    @allure.story("Message structure")
    def test_kafka_message_structure(self, kafka_client: KafkaClient):
        """Проверка структуры сообщений в топике 'users'."""
        with allure.step("Получение последних сообщений из топика 'users'"):
            messages = kafka_client.get_latest_messages(
                topic=KafkaClient.TOPIC_USERS,
                count=5,
            )

        with allure.step("Проверка структуры сообщений"):
            allure.attach(
                f"Получено сообщений: {len(messages)}\n{messages}",
                name="kafka_messages",
                attachment_type=allure.attachment_type.TEXT,
            )
            for msg in messages:
                if isinstance(msg, dict):
                    assert "username" in msg, (
                        f"Каждое сообщение должно содержать поле 'username', получено: {msg}"
                    )

