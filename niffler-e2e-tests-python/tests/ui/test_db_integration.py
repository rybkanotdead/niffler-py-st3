import pytest
import allure
from faker import Faker
from selene import browser

from pages.category_page import CategoryPage

faker = Faker()
category_page = CategoryPage()


@allure.feature("Интеграция с Базой Данных")
@allure.story("Управление категориями")
class TestDBIntegration:

    @pytest.fixture
    def new_category_name(self):
        return faker.word() + "_" + faker.bothify(text='??##')

    @allure.title("Создание категории через UI и валидация записи в БД")
    def test_create_category_check_in_db(self, login_user, profile_page, db, envs, new_category_name):
        username = envs['test_username']

        with allure.step(f"UI: Создать новую категорию '{new_category_name}' в профиле"):
            profile_page.add_category(new_category_name)
            profile_page.successful_adding(new_category_name)

        with allure.step(f"DB: Проверить, что категория '{new_category_name}' сохранена в базе"):
            db_record = db.get_category(username, new_category_name)

            assert db_record is not None, f"Категория {new_category_name} не найдена в БД!"

            with allure.step("Сверить поля записи (name, username, archived)"):
                assert db_record['name'] == new_category_name
                assert db_record['username'] == username
                assert db_record['archived'] is False

        with allure.step("Post-condition: Удалить созданную категорию из БД"):
            db.delete_category(username, new_category_name)

    @allure.title("Архивация категории и проверка смены статуса в БД")
    def test_archive_category_check_db_state(self, login_user, profile_page, db, envs):
        username = envs['test_username']
        cat_name = "Arch_Test_" + faker.bothify(text='####')

        with allure.step(f"Pre-condition: Создать категорию '{cat_name}' напрямую через БД"):
            db.insert_category(username, cat_name)

        with allure.step("UI: Обновить страницу и архивировать категорию"):
            browser.driver.refresh()  # Обновляем, чтобы подтянуть данные из БД
            category_page.archive_category(cat_name)
            category_page.check_category_not_visible(cat_name)

        with allure.step("DB: Проверить, что статус категории изменился на archived=True"):
            db_record = db.get_category(username, cat_name)
            assert db_record is not None, "Запись пропала из БД!"
            assert db_record['archived'] is True, "Флаг archived в БД не обновился!"

        with allure.step("Post-condition: Удалить тестовую запись"):
            db.delete_category(username, cat_name)