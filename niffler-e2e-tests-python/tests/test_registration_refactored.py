"""
Рефакторенные тесты регистрации нового пользователя.
Используют вспомогательные функции для улучшения читаемости и поддержки.
"""
import allure
from selene import be, have
from helpers.registration_helper import RegistrationHelper, LoginHelper
from faker import Faker

faker = Faker()


@allure.feature("Регистрация")
@allure.story("Создание нового аккаунта")
@allure.severity(allure.severity_level.CRITICAL)
class TestUserRegistration:
    """Тесты на регистрацию нового пользователя"""

    @allure.title("Успешная регистрация с валидными данными")
    @allure.description("""
        Проверяет полный флоу регистрации нового пользователя:
        1. Открытие формы регистрации
        2. Заполнение всех полей
        3. Отправка формы
        4. Перенаправление на страницу логина
    """)
    @allure.tag("smoke", "registration", "positive")
    def test_successful_registration(self, auth_page):
        # Arrange - подготовка данных
        credentials = RegistrationHelper.generate_user_credentials()
        
        # Act - выполнение действий
        RegistrationHelper.complete_registration(
            auth_page,
            credentials['username'],
            credentials['password']
        )
        
        # Assert - проверка результата
        with allure.step("ОР: Пользователь перенаправлен на страницу логина"):
            auth_page.login_btn.should(have.text("Log in"))

    @allure.title("Регистрация: пошаговое заполнение формы")
    @allure.description("""
        Детальная проверка каждого шага регистрации для отладки.
        Тест специально разбит на мелкие шаги для понятного отчета.
    """)
    @allure.tag("registration", "detailed", "positive")
    def test_registration_step_by_step(self, auth_page):
        # Шаг 1: Генерация данных
        credentials = RegistrationHelper.generate_user_credentials()
        username = credentials['username']
        password = credentials['password']
        
        # Шаг 2: Открытие формы
        with allure.step(f"Открыть страницу регистрации"):
            auth_page.open_auth_page()
            
        with allure.step("Нажать кнопку 'Create new account'"):
            auth_page.to_register_btn.click()
            
        with allure.step("Проверить, что открылась форма регистрации"):
            auth_page.register_btn.should(have.text("Sign Up"))
        
        # Шаг 3: Заполнение полей по одному
        with allure.step(f"Ввести логин: {username}"):
            auth_page.username.type(username)
            auth_page.username.should(have.value(username))
            
        with allure.step("Ввести пароль"):
            auth_page.password.type(password)
            auth_page.password.should(have.value(password))
            
        with allure.step("Подтвердить пароль"):
            auth_page.pass_submit.type(password)
            auth_page.pass_submit.should(have.value(password))
        
        # Шаг 4: Отправка формы
        with allure.step("Нажать кнопку Sign Up"):
            auth_page.register_btn.click()
        
        # Шаг 5: Проверка результата
        with allure.step("ОР: Пользователь перенаправлен на страницу логина"):
            auth_page.login_btn.should(have.text("Log in"))


@allure.feature("Регистрация")
@allure.story("Перенос данных между формами")
@allure.severity(allure.severity_level.NORMAL)
class TestDataTransferBetweenForms:
    """Тесты на сохранение данных при переходе между формами"""

    @allure.title("Данные сохраняются при переходе с логина на регистрацию")
    @allure.description("""
        Проверяет UX-фичу: если пользователь начал вводить данные на форме логина,
        а затем решил зарегистрироваться - данные должны сохраниться.
    """)
    @allure.tag("ux", "data-transfer", "positive")
    def test_login_to_registration_data_transfer(self, auth_page):
        # Arrange
        credentials = RegistrationHelper.generate_user_credentials()
        username = credentials['username']
        password = credentials['password']
        
        # Act - заполнить форму логина
        with allure.step("Открыть страницу логина"):
            auth_page.open_auth_page()
            
        LoginHelper.fill_login_form(auth_page, username, password)
        
        with allure.step("Перейти на форму регистрации"):
            auth_page.to_register_btn.click()
        
        # Assert - проверить сохранение данных
        with allure.step("ОР: Логин сохранился"):
            auth_page.username.should(have.value(username))
            
        with allure.step("ОР: Пароль сохранился"):
            auth_page.password.should(have.value(password))

    @allure.title("Данные сохраняются при переходе с регистрации на логин")
    @allure.description("""
        Обратная проверка: переход с регистрации на логин также должен сохранять данные.
    """)
    @allure.tag("ux", "data-transfer", "positive")
    def test_registration_to_login_data_transfer(self, auth_page):
        # Arrange
        credentials = RegistrationHelper.generate_user_credentials()
        username = credentials['username']
        password = credentials['password']
        
        # Act - заполнить форму регистрации
        with allure.step("Открыть форму регистрации"):
            RegistrationHelper.open_registration_form(auth_page)
            
        with allure.step(f"Заполнить логин и пароль"):
            auth_page.username.type(username)
            auth_page.password.type(password)
        
        with allure.step("Вернуться на форму логина"):
            auth_page.to_login_btn.click()
        
        # Assert - проверить сохранение данных
        with allure.step("ОР: Данные сохранились при возврате на логин"):
            auth_page.username.should(have.value(username))
            auth_page.password.should(have.value(password))


@allure.feature("Регистрация")
@allure.story("Негативные сценарии")
@allure.severity(allure.severity_level.NORMAL)
class TestRegistrationNegative:
    """Негативные тесты регистрации"""

    @allure.title("Регистрация с несовпадающими паролями")
    @allure.description("Пароли в полях Password и Submit password должны совпадать")
    @allure.tag("negative", "validation")
    def test_password_mismatch(self, auth_page):
        # Arrange
        username = faker.user_name()
        password = faker.password(length=8)
        wrong_password = faker.password(length=8)
        
        # Act
        RegistrationHelper.open_registration_form(auth_page)
        
        with allure.step(f"Ввести разные пароли"):
            auth_page.username.type(username)
            auth_page.password.type(password)
            auth_page.pass_submit.type(wrong_password)
            auth_page.register_btn.click()
        
        # Assert
        with allure.step("ОР: Отображается ошибка о несовпадении паролей"):
            auth_page.form_error.should(be.visible)

    @allure.title("Регистрация с пустыми полями")
    @allure.description("Все обязательные поля должны быть заполнены")
    @allure.tag("negative", "validation")
    def test_empty_fields(self, auth_page):
        # Act
        RegistrationHelper.open_registration_form(auth_page)
        
        with allure.step("Нажать Sign Up без заполнения полей"):
            auth_page.register_btn.click()
        
        # Assert
        with allure.step("ОР: Форма регистрации все еще видна"):
            auth_page.register_btn.should(be.visible)
