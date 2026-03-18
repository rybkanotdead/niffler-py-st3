"""
API тесты с проверкой в БД.

Тесты проверяют:
1. Создание категорий через API с проверкой в БД
2. Создание трат через API с проверкой в БД
3. Удаление категорий через API с проверкой в БД
4. Обновление состояния в БД после API операций
"""
import pytest
import allure
from faker import Faker

faker = Faker()


@pytest.mark.api
@pytest.mark.db
@pytest.mark.integration
class TestCategoryAPIWithDB:
    """Тесты API категорий с проверкой в БД."""

    @allure.title("Создание категории через API с проверкой в БД")
    @allure.description(
        """
        Предусловие: пользователь авторизован
        Шаги:
        1. Создаем категорию через REST API
        2. Проверяем успешный ответ API
        3. Проверяем, что категория добавлена в БД
        4. Проверяем корректность данных категории в БД
        
        Ожидается: Категория успешно создана в API и добавлена в БД
        """
    )
    def test_create_category_via_api_verify_in_db(
            self,
            category_client,
            db,
            existed_user_credentials,
            cleanup_categories
    ):
        """Создание категории через API с проверкой в БД."""
        username = existed_user_credentials['username']
        category_name = f"api_cat_{faker.word()}_{faker.bothify(text='####')}"

        with allure.step(f"Создание категории '{category_name}' через API"):
            category_response = category_client.add_category(category_name)
            
            with allure.step("Проверка ответа API"):
                assert category_response is not None
                assert category_response['name'] == category_name

        with allure.step("Проверка категории в БД"):
            db_record = db.get_category(username, category_name)
            
            assert db_record is not None, f"Категория {category_name} не найдена в БД!"
            assert db_record['name'] == category_name
            assert db_record['username'] == username

        with allure.step("Добавление категории в список для очистки"):
            cleanup_categories.append(category_response['id'])

    @allure.title("Получение категорий через API и проверка в БД")
    @allure.description(
        """
        Предусловие: 
        1. Пользователь авторизован
        2. В БД существует несколько категорий
        
        Шаги:
        1. Получаем список всех категорий через API
        2. Получаем список категорий из БД
        3. Сравниваем количество и содержимое категорий
        
        Ожидается: Данные из API совпадают с БД
        """
    )
    def test_get_categories_api_matches_db(
            self,
            category_client,
            db,
            existed_user_credentials
    ):
        """Проверка, что API возвращает то же, что в БД."""
        username = existed_user_credentials['username']

        with allure.step("Получение категорий через API"):
            api_categories = category_client.get_categories()

        with allure.step("Получение категорий из БД"):
            db_categories = db.get_user_categories(username)

        with allure.step("Сравнение количества категорий"):
            assert len(api_categories) == len(db_categories), \
                "Количество категорий в API и БД не совпадает"

        with allure.step("Сравнение имен категорий"):
            api_names = {cat['name'] for cat in api_categories}
            db_names = {cat['name'] for cat in db_categories}
            assert api_names == db_names, "Имена категорий не совпадают"


@pytest.mark.api
@pytest.mark.db
@pytest.mark.integration
class TestSpendingAPIWithDB:
    """Тесты API трат с проверкой в БД."""

    @allure.title("Создание траты через API с проверкой в БД")
    @allure.description(
        """
        Предусловие:
        1. Пользователь авторизован
        2. В системе существует категория
        
        Шаги:
        1. Создаем трату через REST API
        2. Проверяем успешный ответ API
        3. Проверяем, что траты добавлена в БД
        4. Проверяем корректность всех данных в БД
        
        Ожидается: Траты успешно создана в API и добавлена в БД
        """
    )
    def test_create_spending_via_api_verify_in_db(
            self,
            spends_client,
            db,
            existed_user_credentials,
            cleanup_db_spends
    ):
        """Создание траты через API с проверкой в БД."""
        username = existed_user_credentials['username']
        amount = 250.75
        description = f"API spending {faker.word()}"
        category = "Travel"
        currency = "USD"

        with allure.step(f"Создание траты через API"):
            spend_response = spends_client.add_spends(
                amount=amount,
                description=description,
                category=category,
                currency=currency
            )
            
            with allure.step("Проверка ответа API"):
                assert spend_response is not None
                assert spend_response['amount'] == amount
                assert spend_response['description'] == description

        with allure.step("Проверка траты в БД"):
            db_spends = db.get_user_spends(username)
            
            spend_record = None
            for spend in db_spends:
                if str(spend['id']) == str(spend_response['id']):
                    spend_record = spend
                    break
            
            assert spend_record is not None, f"Траты не найдена в БД!"
            assert spend_record['amount'] is not None, "Сумма не должна быть None"
            assert float(str(spend_record['amount'])) == amount, "Сумма не совпадает"
            assert spend_record['description'] == description, "Описание не совпадает"
            assert spend_record['currency'] == currency, "Валюта не совпадает"

        with allure.step("Добавление траты в список для очистки"):
            cleanup_db_spends.append(str(spend_response['id']))

    @allure.title("Удаление траты через API с проверкой в БД")
    @allure.description(
        """
        Предусловие:
        1. Пользователь авторизован
        2. В БД существует траты
        
        Шаги:
        1. Создаем трату через API
        2. Удаляем трату через API
        3. Проверяем, что траты удалена из БД
        
        Ожидается: Траты удалена как из API, так и из БД
        """
    )
    def test_delete_spending_via_api_verify_in_db(
            self,
            spends_client,
            db,
            existed_user_credentials
    ):
        """Удаление траты через API с проверкой в БД."""
        username = existed_user_credentials['username']
        description = f"API delete test {faker.word()}"

        with allure.step("Создание траты для удаления"):
            spend_response = spends_client.add_spends(
                amount=100.00,
                description=description,
                category="Test",
                currency="RUB"
            )
            spend_id = spend_response['id']

        with allure.step("Проверка, что траты находится в БД"):
            db_spend = db.get_spend_by_id(spend_id)
            assert db_spend is not None, "Траты должна быть в БД"

        with allure.step("Удаление траты через API"):
            spends_client.remove_spends([spend_id])

        with allure.step("Проверка, что траты удалена из БД"):
            db_spend = db.get_spend_by_id(spend_id)
            assert db_spend is None, "Траты должна быть удалена из БД"

    @allure.title("Получение всех трат через API и проверка в БД")
    @allure.description(
        """
        Предусловие:
        1. Пользователь авторизован
        2. В БД существует несколько трат
        
        Шаги:
        1. Получаем список всех трат через API
        2. Получаем список трат из БД
        3. Сравниваем количество и содержимое трат
        
        Ожидается: Данные из API совпадают с БД
        """
    )
    def test_get_spendings_api_matches_db(
            self,
            spends_client,
            db,
            existed_user_credentials
    ):
        """Проверка, что API возвращает то же, что в БД."""
        username = existed_user_credentials['username']

        with allure.step("Получение трат через API"):
            api_spends = spends_client.get_spends()

        with allure.step("Получение трат из БД"):
            db_spends = db.get_user_spends(username)

        with allure.step("Сравнение количества трат"):
            assert len(api_spends) == len(db_spends), \
                "Количество трат в API и БД не совпадает"

        with allure.step("Сравнение ID трат"):
            api_ids = {str(spend['id']) for spend in api_spends}
            db_ids = {str(spend['id']) for spend in db_spends}
            assert api_ids == db_ids, "ID трат не совпадают"

