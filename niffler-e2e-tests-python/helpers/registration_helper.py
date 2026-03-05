"""
Вспомогательные функции для работы с регистрацией и авторизацией.
Разделение бизнес-логики и тестов для улучшения читаемости.
"""
import allure
from faker import Faker

faker = Faker()


class RegistrationHelper:
    """Помощник для работы с регистрацией пользователей"""

    @staticmethod
    def generate_user_credentials():
        """
        Генерирует валидные учетные данные пользователя
        
        Returns:
            dict: Словарь с username и password
        """
        with allure.step("Сгенерировать учетные данные"):
            return {
                'username': faker.user_name(),
                'password': faker.password(length=8)
            }

    @staticmethod
    def open_registration_form(auth_page):
        """
        Открывает форму регистрации из страницы авторизации
        
        Args:
            auth_page: Объект страницы авторизации
        """
        with allure.step("Открыть форму регистрации"):
            auth_page.open_auth_page()
            auth_page.to_register_btn.click()

    @staticmethod
    def fill_registration_form(auth_page, username, password):
        """
        Заполняет форму регистрации данными
        
        Args:
            auth_page: Объект страницы авторизации
            username: Имя пользователя
            password: Пароль
        """
        with allure.step(f"Заполнить форму регистрации для пользователя: {username}"):
            auth_page.username.type(username)
            auth_page.password.type(password)
            auth_page.pass_submit.type(password)

    @staticmethod
    def submit_registration(auth_page):
        """
        Отправляет форму регистрации
        
        Args:
            auth_page: Объект страницы авторизации
        """
        with allure.step("Нажать кнопку Sign Up"):
            auth_page.register_btn.click()

    @staticmethod
    def complete_registration(auth_page, username=None, password=None):
        """
        Полный цикл регистрации пользователя
        
        Args:
            auth_page: Объект страницы авторизации
            username: Имя пользователя (опционально, генерируется автоматически)
            password: Пароль (опционально, генерируется автоматически)
            
        Returns:
            dict: Учетные данные созданного пользователя
        """
        credentials = {
            'username': username or faker.user_name(),
            'password': password or faker.password(length=8)
        }
        
        RegistrationHelper.open_registration_form(auth_page)
        RegistrationHelper.fill_registration_form(
            auth_page, 
            credentials['username'], 
            credentials['password']
        )
        RegistrationHelper.submit_registration(auth_page)
        
        return credentials


class LoginHelper:
    """Помощник для работы с авторизацией"""

    @staticmethod
    def fill_login_form(auth_page, username, password):
        """
        Заполняет форму входа данными
        
        Args:
            auth_page: Объект страницы авторизации
            username: Имя пользователя
            password: Пароль
        """
        with allure.step(f"Заполнить форму входа для пользователя: {username}"):
            auth_page.username.type(username)
            auth_page.password.type(password)

    @staticmethod
    def verify_login_success(spending_page, auth_page):
        """
        Проверяет успешный вход в систему
        
        Args:
            spending_page: Объект страницы расходов
            auth_page: Объект страницы авторизации
        """
        from selene import be
        with allure.step("Проверить успешную авторизацию"):
            spending_page.stat_area.should(be.visible)
            auth_page.login_btn.should(be.not_.visible)

    @staticmethod
    def verify_login_failed(auth_page, error_text="Bad credentials"):
        """
        Проверяет неуспешный вход в систему
        
        Args:
            auth_page: Объект страницы авторизации
            error_text: Ожидаемый текст ошибки
        """
        from selene import be, have
        with allure.step(f"Проверить ошибку авторизации: {error_text}"):
            auth_page.form_error.should(be.visible)
            auth_page.form_error.should(have.text(error_text))
            auth_page.login_btn.should(be.visible)
