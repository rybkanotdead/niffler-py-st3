import allure
from marks import Pages
from faker import Faker

faker = Faker()


@allure.feature("Профиль пользователя")
@allure.story("Управление категориями")
class TestCategories:

    @allure.title("Создание новой категории")
    @Pages.profile_page
    def test_create_category(self, profile_page):
        new_category = faker.word()

        with allure.step(f"Добавить новую категорию: '{new_category}'"):
            profile_page.add_category(new_category)

        with allure.step(f"ОР: Категория '{new_category}' успешно отображается в списке"):
            profile_page.successful_adding(new_category)

    @allure.title("Попытка добавления категории с пустым именем")
    @Pages.profile_page
    def test_add_empty_name_category(self, profile_page):
        with allure.step("Нажать кнопку добавления категории без ввода названия"):
            profile_page.adding_empty_name_category()

        with allure.step("ОР: Отображается сообщение об ошибке валидации"):
            profile_page.check_error_message("Error while adding category : Category can not be blank")


@allure.feature("Профиль пользователя")
@allure.story("Редактирование личных данных")
class TestProfileInfo:

    @allure.title("Проверка заголовка страницы профиля")
    @Pages.profile_page
    def test_profile_title(self, profile_page):
        with allure.step("ОР: Заголовок страницы содержит текст 'Profile'"):
            profile_page.check_profile_title('Profile')

    @allure.title("Изменение имени пользователя (First Name)")
    @Pages.profile_page
    def test_create_user_name(self, profile_page):
        user_name = faker.first_name()

        with allure.step(f"Изменить имя пользователя на '{user_name}'"):
            profile_page.add_user_name(user_name)

        with allure.step(f"ОР: Имя пользователя успешно обновлено на '{user_name}'"):

            profile_page.check_successful_adding_name(user_name)
