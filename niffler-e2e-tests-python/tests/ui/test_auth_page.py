import allure
from selene import be, have
from faker import Faker


faker = Faker()


@allure.feature("Авторизация и Регистрация")
@allure.story("Сценарии входа и выхода из системы")
class TestAuthPage:

    @allure.title("Успешная авторизация существующим пользователем")
    def test_login(self, auth_page, spending_page, existed_user_credentials):
        auth_page.login(
            existed_user_credentials.get('username'),
            existed_user_credentials.get('password')
        )

        with allure.step("ОР: Пользователь успешно авторизован, видна статистика"):
            spending_page.stat_area.should(be.visible)
            auth_page.login_btn.should(be.not_.visible)

    @allure.title("Выход из системы (Logout)")
    def test_logout(self, auth_page, spending_page):
        auth_page.login_as_standard_user()

        spending_page.logout()

        with allure.step("ОР: Пользователь разлогинен, видна кнопка регистрации"):
            auth_page.to_register_btn.should(be.visible)
            auth_page.login_btn.should(have.text("Log in"))

    @allure.title("Авторизация с невалидными данными")
    def test_login_invalid_creds(self, auth_page):
        auth_page.login(faker.user_name(), faker.password())

        with allure.step("ОР: Ошибка авторизации, вход не выполнен"):
            auth_page.form_error.should(be.visible)
            auth_page.form_error.should(have.text("Bad credentials"))  # или ваш текст ошибки
            auth_page.login_btn.should(be.visible)

    @allure.title("Авторизация с пустыми полями")
    def test_login_empty_fields(self, auth_page):
        auth_page.login_btn.click()

        with allure.step("ОР: Вход не выполнен, поля остались пустыми"):
            auth_page.login_btn.should(be.visible)

    @allure.title("Переключение между формами регистрации и логина")
    def test_switch_between_login_and_register(self, auth_page):
        auth_page.to_register_btn.click()

        with allure.step("ОР: Открыта форма регистрации"):
            auth_page.register_btn.should(have.text("Sign Up"))

        auth_page.to_login_btn.click()

        with allure.step("ОР: Открыта форма логина"):
            auth_page.login_btn.should(have.text("Log in"))