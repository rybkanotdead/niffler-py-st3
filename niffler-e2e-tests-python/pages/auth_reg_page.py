import os
import allure
from selene import browser, by, have


class AuthRegistrationPage:

    def __init__(self):
        self.username = browser.element('input[name=username]')
        self.password = browser.element('input[name=password]')
        self.pass_submit = browser.element('#passwordSubmit')
        self.login_btn = browser.element('button[type="submit"]')  # Обновил селектор для надежности
        self.register_btn = browser.element('.form__submit')

        self.to_register_btn = browser.element('[href="/register"]')
        self.to_login_btn = browser.element('[href="/login"]')

        self.form_error = browser.element('.form__error')

    def open_auth_page(self):
        with allure.step('Открыть страницу авторизации'):
            browser.open('/login')

    def fill_username(self, username: str):
        with allure.step(f'Заполнить логин: {username}'):
            self.username.type(username)

    def fill_password(self, password: str):
        with allure.step('Заполнить пароль'):
            self.password.type(password)

    def click_sign_up_btn(self):
        with allure.step('Нажать кнопку регистрации/входа'):
            self.login_btn.click()

    # === ИСПРАВЛЕНИЕ ОШИБОК ===

    def login(self, username, password):
        """Метод для авторизации с передачей данных"""
        with allure.step(f'Авторизация пользователя {username}'):
            self.open_auth_page()
            self.fill_username(username)
            self.fill_password(password)
            self.login_btn.click()

    def login_as_standard_user(self):
        """Быстрый вход под тестовым пользователем из .env"""
        user = os.getenv('TEST_USERNAME')
        pwd = os.getenv('TEST_PASSWORD')
        with allure.step('Быстрая авторизация стандартным пользователем'):
            self.login(user, pwd)