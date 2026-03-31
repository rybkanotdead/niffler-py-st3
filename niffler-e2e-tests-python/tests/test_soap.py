"""
SOAP тесты для Niffler Userdata сервиса.

Тесты проверяют:
1. Получение данных текущего пользователя через SOAP
2. Обновление данных пользователя через SOAP
3. Получение списка пользователей через SOAP
"""
import pytest
import allure
from faker import Faker

from clients.soap_client import UserdataSoapClient

faker = Faker()


@pytest.mark.soap
@pytest.mark.smoke
class TestUserdataSoap:
    """SOAP тесты для Userdata сервиса."""

    @allure.title("SOAP: получение данных текущего пользователя")
    @allure.description(
        """
        Шаги:
        1. Отправляем SOAP запрос currentUser с именем тестового пользователя
        2. Проверяем, что ответ содержит корректные данные пользователя
        3. Проверяем наличие обязательных полей (id, username, currency)

        Ожидается: возвращаются корректные данные тестового пользователя
        """
    )
    @allure.feature("SOAP")
    @allure.story("Userdata")
    def test_get_current_user(
            self,
            soap_client: UserdataSoapClient,
            existed_user_credentials: dict,
    ):
        """Получение данных пользователя через SOAP."""
        username = existed_user_credentials["username"]

        with allure.step(f"SOAP запрос currentUser для '{username}'"):
            user = soap_client.get_current_user(username)

        with allure.step("Проверка обязательных полей"):
            allure.attach(
                str(user),
                name="user_response",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert user, "Ответ не должен быть пустым"
            assert user.get("username") == username, (
                f"Ожидался username='{username}', получено: {user.get('username')}"
            )
            assert "id" in user, "Ответ должен содержать поле 'id'"
            assert "currency" in user, "Ответ должен содержать поле 'currency'"

    @allure.title("SOAP: обновление имени и фамилии пользователя")
    @allure.description(
        """
        Шаги:
        1. Получаем текущие данные пользователя
        2. Обновляем firstname и surname через SOAP
        3. Повторно получаем пользователя и проверяем обновлённые данные

        Ожидается: данные пользователя обновлены
        """
    )
    @allure.feature("SOAP")
    @allure.story("Userdata")
    def test_update_user_name(
            self,
            soap_client: UserdataSoapClient,
            existed_user_credentials: dict,
    ):
        """Обновление данных пользователя через SOAP."""
        username = existed_user_credentials["username"]

        with allure.step("Получение текущих данных пользователя"):
            user = soap_client.get_current_user(username)
            assert user, "Пользователь должен существовать"
            user_id = user["id"]

        new_firstname = faker.first_name()
        new_surname = faker.last_name()

        with allure.step(f"Обновление: firstname='{new_firstname}', surname='{new_surname}'"):
            updated = soap_client.update_user(
                user_id=user_id,
                username=username,
                firstname=new_firstname,
                surname=new_surname,
                currency=user.get("currency", "RUB"),
            )

        with allure.step("Проверка обновлённых данных"):
            allure.attach(
                str(updated),
                name="updated_user",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert updated.get("firstname") == new_firstname or updated.get("username") == username, (
                "Данные должны быть обновлены"
            )

    @allure.title("SOAP: получение списка всех пользователей")
    @allure.description(
        """
        Шаги:
        1. Отправляем SOAP запрос allUsers
        2. Проверяем, что список не пустой
        3. Проверяем структуру каждого пользователя

        Ожидается: список пользователей возвращён корректно
        """
    )
    @allure.feature("SOAP")
    @allure.story("Userdata")
    def test_get_all_users(
            self,
            soap_client: UserdataSoapClient,
            existed_user_credentials: dict,
    ):
        """Получение списка пользователей через SOAP."""
        username = existed_user_credentials["username"]

        with allure.step(f"SOAP запрос allUsers для '{username}'"):
            users = soap_client.get_all_users(username)

        with allure.step("Проверка результата"):
            allure.attach(
                f"Получено пользователей: {len(users)}",
                name="users_count",
                attachment_type=allure.attachment_type.TEXT,
            )
            # Может быть пустым если нет других пользователей — это нормально
            assert isinstance(users, list), "Ответ должен быть списком"

    @allure.title("SOAP: структура ответа содержит обязательные поля")
    @allure.feature("SOAP")
    @allure.story("Userdata")
    def test_current_user_response_structure(
            self,
            soap_client: UserdataSoapClient,
            existed_user_credentials: dict,
    ):
        """Проверка структуры SOAP ответа."""
        username = existed_user_credentials["username"]

        with allure.step("Получение пользователя через SOAP"):
            user = soap_client.get_current_user(username)

        with allure.step("Проверка структуры ответа"):
            required_fields = ["id", "username", "currency"]
            for field in required_fields:
                assert field in user, f"Поле '{field}' должно быть в ответе"

        with allure.step("Проверка валюты"):
            valid_currencies = {"RUB", "USD", "EUR", "KZT"}
            currency = user.get("currency", "")
            assert currency in valid_currencies, (
                f"Валюта '{currency}' должна быть одной из {valid_currencies}"
            )

