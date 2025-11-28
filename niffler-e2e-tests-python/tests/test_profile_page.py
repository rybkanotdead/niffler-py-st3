from selene import be, have
from marks import Pages, TestData
from faker import Faker

faker = Faker()

TEST_CATEGORY = "school"


class TestCategories:

    @Pages.profile_page
    def test_create_category(self, profile_page):
        """Тест: создание новой категории"""
        new_category = faker.word()
        profile_page.add_category(new_category)
        profile_page.successful_adding(new_category)

    @Pages.profile_page
    def test_add_empty_name_category(self, profile_page):
        """Тест: попытка добавления категории с пустым именем"""
        profile_page.adding_empty_name_category()
        profile_page.check_error_message("Error while adding category : Category can not be blank")


class TestProfileInfo:

    @Pages.profile_page
    def test_profile_title(self, profile_page):
        """Тест: проверка заголовка профиля"""
        profile_page.check_profile_title('Profile')

    @Pages.profile_page
    def test_create_user_name(self, profile_page):
        """Тест: добавление имени пользователя в профиль"""
        user_name = faker.user_name()
        profile_page.add_user_name(user_name)
        profile_page.check_successful_adding_name()