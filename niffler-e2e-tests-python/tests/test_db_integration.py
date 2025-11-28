import pytest
from faker import Faker
from selene import browser, have

from pages.category_page import CategoryPage

faker = Faker()
category_page = CategoryPage()


class TestDBIntegration:

    @pytest.fixture
    def new_category_name(self):
        return faker.word() + "_" + faker.bothify(text='??##')

    def test_create_category_check_in_db(self, login_user, profile_page, db, envs, new_category_name):
        username = envs['test_username']

        profile_page.add_category(new_category_name)
        profile_page.successful_adding(new_category_name)

        db_record = db.get_category(username, new_category_name)

        assert db_record is not None, f"Категория {new_category_name} не найдена в БД!"
        assert db_record['name'] == new_category_name
        assert db_record['username'] == username
        assert db_record['archived'] is False

        db.delete_category(username, new_category_name)

    def test_archive_category_check_db_state(self, login_user, profile_page, db, envs):

        username = envs['test_username']
        cat_name = "Arch_Test_" + faker.bothify(text='####')

        db.insert_category(username, cat_name)

        browser.driver.refresh()

        category_page.archive_category(cat_name)
        category_page.check_category_not_visible(cat_name)

        db_record = db.get_category(username, cat_name)

        assert db_record['archived'] is True, "Флаг archived в БД должен стать True!"

        db.delete_category(username, cat_name)