import pytest
import allure
from modals.category import CategorySQL
from modals.enums import Category
# Советую использовать стандартные assert python, если api_assertions
# не делают какой-то специфической магии или мягких проверок
from utils.api_assertions import assertEqual


@allure.feature('Категории')
@allure.story('API')
class TestCategoryApi:

    @pytest.fixture
    def created_category(self, spends_client):
        """Фикстура: создает категорию и возвращает ее объект"""
        with allure.step('Setup: Создать категорию для теста'):
            return spends_client.add_category(Category.TEST_CATEGORY)

    @allure.title('Создание категории через API')
    def test_add_category_api(self, spends_client, envs, clean_categories):
        with allure.step('Отправить запрос на создание категории'):
            added_category = spends_client.add_category(Category.TEST_CATEGORY)

        with allure.step('Проверить ответ'):
            assertEqual(added_category.name, Category.TEST_CATEGORY,
                        "Имя категории совпадает")
            assertEqual(added_category.username, envs.niffler_username,
                        "Категория привязана к пользователю")
            # Хорошая практика проверять, что ID пришел (не None)
            assert added_category.id is not None, "ID категории не пустой"

    @allure.title('Получение списка категорий через API')
    def test_get_categories_api(self, spends_client, clean_categories):
        # Arrange
        with allure.step('Подготовка данных (создание 2-х категорий)'):
            cat_1 = spends_client.add_category(Category.TEST_CATEGORY)
            cat_2 = spends_client.add_category(Category.TEST_CATEGORY_2)

        # Act
        with allure.step('Получить список категорий'):
            categories_list = spends_client.get_categories()

        # Assert (Безопасная проверка)
        with allure.step('Проверить наличие созданных категорий в списке'):
            # Собираем список ID из ответа
            response_ids = [c.id for c in categories_list]

            assert cat_1.id in response_ids, f"Категория {cat_1.name} не найдена в списке"
            assert cat_2.id in response_ids, f"Категория {cat_2.name} не найдена в списке"

    @allure.title('Редактирование названия категории через API')
    def test_edit_category_name_api(self, spends_client, created_category):
        # Arrange: используем фикстуру created_category, чтобы не писать код создания
        new_name = Category.TEST_CATEGORY_2

        edit_data = CategorySQL(
            id=created_category.id,
            name=new_name,
            username=created_category.username,
            archived=False
        )

        # Act
        with allure.step(f'Изменить имя категории на {new_name}'):
            updated_category = spends_client.edit_category(edit_data)

        # Assert
        assertEqual(updated_category.name, new_name, "Имя категории обновилось")

    @allure.title('Помещение в архив категории через API')
    def test_edit_category_archive_api(self, spends_client, created_category):
        # Arrange
        edit_data = CategorySQL(
            id=created_category.id,
            name=created_category.name,  # Оставляем имя прежним, тестируем только флаг
            username=created_category.username,
            archived=True
        )

        # Act
        with allure.step('Архивировать категорию'):
            archived_category = spends_client.edit_category(edit_data)

        # Assert
        assertEqual(archived_category.archived, True, "Флаг archived равен True")