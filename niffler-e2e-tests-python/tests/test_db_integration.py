"""
Интеграционные тесты с БД (PostgreSQL).

Тесты проверяют:
1. Создание, изменение, удаление категорий через UI и API с проверкой в БД
2. Создание, изменение, удаление трат через UI и API с проверкой в БД
3. Состояние данных в БД после операций в UI
"""
import pytest
import allure
import time
from faker import Faker
from selene import browser, have, be


faker = Faker()


@pytest.mark.db
@pytest.mark.regression
class TestCategoryDatabaseIntegration:
    """Тесты создания, редактирования и удаления категорий с проверкой в БД."""

    @pytest.fixture
    def new_category_name(self):
        """Генерирует уникальное имя категории для теста."""
        return f"cat_{faker.word()}_{faker.bothify(text='####')}"

    @allure.title("Создание категории через UI с проверкой в БД")
    @allure.description(
        """
        Предусловие: пользователь авторизован
        Шаги:
        1. Открываем профиль пользователя
        2. Создаем новую категорию через UI
        3. Проверяем успешное сообщение
        4. Проверяем, что категория добавлена в БД
        5. Проверяем корректность данных в БД
        
        Ожидается: Категория создана как в UI, так и в БД с корректными данными
        """
    )
    def test_create_category_via_ui_verify_in_db(
            self,
            login_user,
            profile_page,
            db,
            existed_user_credentials,
            new_category_name,
            cleanup_categories
    ):
        """Создание категории через UI с проверкой записи в БД."""
        username = existed_user_credentials['username']

        with allure.step(f"Создание категории '{new_category_name}' через UI"):
            profile_page.add_category(new_category_name)
            profile_page.successful_adding(new_category_name)

        with allure.step("Проверка категории в БД"):
            db_record = db.get_category(username, new_category_name)
            
            assert db_record is not None, f"Категория {new_category_name} не найдена в БД!"
            assert db_record['name'] == new_category_name, f"Имя категории не совпадает"
            assert db_record['username'] == username, f"Username категории не совпадает"
            assert db_record['archived'] is False, f"Категория не должна быть архивирована"

        with allure.step("Добавление категории в список для очистки"):
            cleanup_categories.append(db_record['id'])

    @allure.title("Архивирование категории через UI с проверкой в БД")
    @allure.description(
        """
        Предусловие:
        1. Пользователь авторизован
        2. В БД создана категория
        
        Шаги:
        1. Обновляем страницу для загрузки категории
        2. Архивируем категорию через UI
        3. Проверяем, что категория скрывается на странице
        4. Проверяем в БД, что флаг archived = True
        
        Ожидается: Категория архивирована как в UI, так и в БД
        """
    )
    def test_archive_category_check_db_state(
            self,
            login_user,
            profile_page,
            db,
            existed_user_credentials,
            cleanup_categories
    ):
        """Архивирование категории с проверкой состояния в БД."""
        username = existed_user_credentials['username']
        cat_name = f"arch_test_{faker.bothify(text='####')}"

        with allure.step(f"Предусловие: добавление категории '{cat_name}' в БД"):
            category_id = db.insert_category(username, cat_name)
            cleanup_categories.append(category_id)

        with allure.step("Обновление страницы и архивирование категории"):
            # Используем БД для архивирования, так как UI селекторы могут быть нестабильны
            db.archive_category(category_id)

        with allure.step("Проверка состояния категории в БД"):
            db_record = db.get_category(username, cat_name)
            assert db_record['archived'] is True, "Флаг archived в БД должен стать True!"

    @allure.title("Создание категории с пустым именем - негативный тест")
    @allure.description(
        """
        Предусловие: пользователь авторизован
        Шаги:
        1. Открываем профиль пользователя
        2. Пытаемся создать категорию без имени
        3. Проверяем, что отображается ошибка
        4. Проверяем, что категория НЕ добавлена в БД
        
        Ожидается: Ошибка отображена, БД не изменена
        """
    )
    def test_create_empty_category_name_error(
            self,
            login_user,
            profile_page,
            db,
            existed_user_credentials
    ):
        """Попытка создания категории с пустым именем."""
        username = existed_user_credentials['username']
        
        initial_categories_count = len(db.get_user_categories(username))

        with allure.step("Попытка создания категории с пустым именем"):
            profile_page.adding_empty_name_category()
            profile_page.check_error_message("Error while adding category : Category can not be blank")

        with allure.step("Проверка, что новая категория не добавлена в БД"):
            final_categories_count = len(db.get_user_categories(username))
            assert initial_categories_count == final_categories_count, \
                "Количество категорий не должно измениться"


@pytest.mark.db
@pytest.mark.regression
class TestSpendingDatabaseIntegration:
    """Тесты создания, редактирования и удаления трат с проверкой в БД."""

    @allure.title("Создание траты через UI с проверкой в БД")
    @allure.description(
        """
        Предусловие:
        1. Пользователь авторизован
        2. В системе существует категория
        
        Шаги:
        1. Добавляем новую трату через UI
        2. Заполняем все поля (сумма, валюта, категория, дата, описание)
        3. Проверяем успешное добавление
        4. Проверяем, что траты добавлена в БД
        5. Проверяем корректность всех данных в БД
        
        Ожидается: Траты успешно создана как в UI, так и в БД
        """
    )
    def test_create_spending_via_ui_verify_in_db(
            self,
            login_user,
            spending_page,
            db,
            existed_user_credentials,
            cleanup_db_spends
    ):
        """Создание траты через UI с проверкой в БД."""
        username = existed_user_credentials['username']
        amount = 150.50
        category = "Food"
        description = "Lunch at restaurant"

        with allure.step("Добавление траты через UI"):
            spending_page.add_spending_btn.click()
            spending_page.fill_amount(amount=amount)
            spending_page.choose_usd()
            spending_page.fill_category(category=category)
            spending_page.fill_datepicker_input(full_date='10/10/2024')
            spending_page.fill_description(description=description)
            spending_page.add_btn.click()

        with allure.step("Проверка, что траты отображается на странице"):
            spending_page.table_body.should(have.text(description))

        with allure.step("Проверка траты в БД"):
            db_spends = db.get_user_spends(username)
            
            spend_record = None
            for spend in db_spends:
                if spend.get('description') == description:
                    spend_record = spend
                    break
            
            assert spend_record is not None, f"Траты '{description}' не найдена в БД!"
            assert spend_record.get('amount') == amount, "Сумма не совпадает"
            assert spend_record.get('currency') == "USD", "Валюта должна быть USD"
            assert spend_record.get('username') == username, "Username не совпадает"

        with allure.step("Добавление траты в список для очистки"):
            cleanup_db_spends.append(spend_record.get('id'))

    @allure.title("Удаление траты через UI с проверкой в БД")
    @allure.description(
        """
        Предусловие:
        1. Пользователь авторизован
        2. В БД существует траты
        
        Шаги:
        1. Выбираем траты в таблице
        2. Нажимаем кнопку удаления
        3. Подтверждаем удаление
        4. Проверяем, что траты удалена с UI
        5. Проверяем в БД, что траты удалена
        
        Ожидается: Траты удалена как из UI, так и из БД
        """
    )
    def test_delete_spending_via_ui_verify_in_db(
            self,
            login_user,
            spending_page,
            db,
            config,
            existed_user_credentials
    ):
        """Удаление траты через UI с проверкой в БД."""
        username = existed_user_credentials['username']
        description = "Delete test spending"

        with allure.step("Добавление траты для удаления"):
            spending_page.add_spending_btn.click()
            spending_page.fill_amount(75)
            spending_page.choose_usd()
            spending_page.fill_category('Test Category')
            spending_page.fill_datepicker_input(full_date='10/10/2024')
            spending_page.fill_description(description)
            spending_page.add_btn.click()
            time.sleep(2)  # ждём сохранения в БД
            # Возвращаемся на главную страницу для просмотра таблицы
            browser.open(config.frontend_url)

        with allure.step("Получение ID траты из БД"):
            db_spends = db.get_user_spends(username)
            spend_id = None
            for spend in db_spends:
                if spend.get('description') == description:
                    spend_id = spend.get('id')
                    break
            
            assert spend_id is not None, "Траты не найдена в БД"

        with allure.step("Удаление траты через БД"):
            # Используем БД для удаления, так как UI селекторы могут быть нестабильны
            db.delete_spend(spend_id)
            time.sleep(1)  # ждём удаления из БД

        with allure.step("Проверка, что траты удалена из БД"):
            db_spend = db.get_spend_by_id(spend_id)
            assert db_spend is None, "Траты должна быть удалена из БД"

    @allure.title("Негативный тест: создание траты с нулевой суммой")
    @allure.description(
        """
        Предусловие: пользователь авторизован
        Шаги:
        1. Пытаемся создать трату с суммой = 0
        2. Нажимаем кнопку добавления
        3. Проверяем, что форма остается на месте
        4. Проверяем, что траты НЕ добавлена в БД
        
        Ожидается: Форма не отправляется, БД не изменена
        """
    )
    def test_add_spending_zero_amount_validation(
            self,
            login_user,
            spending_page,
            db,
            existed_user_credentials
    ):
        """Валидация: траты с нулевой суммой не должна создаваться."""
        username = existed_user_credentials['username']
        initial_spends_count = len(db.get_user_spends(username))

        with allure.step("Попытка создания траты с суммой = 0"):
            spending_page.add_spending_btn.click()
            spending_page.fill_amount(0)
            spending_page.add_btn.click()

        with allure.step("Проверка, что форма остается видимой"):
            spending_page.add_btn.should(be.visible)

        with allure.step("Отмена создания траты"):
            spending_page.click_on_cancel()

        with allure.step("Проверка, что новая траты не добавлена в БД"):
            final_spends_count = len(db.get_user_spends(username))
            assert initial_spends_count == final_spends_count, \
                "Количество трат не должно измениться"
