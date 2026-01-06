import allure
from playwright.sync_api import Page
from pages.base_page import BasePage
from faker import Faker


class RegistrationPage(BasePage):
    def __init__(self, page: Page, auth_url):
        super().__init__(page)
        self.faker = Faker()
        self.auth_url = auth_url

        self.register_link = page.locator("[class='form__register']")
        self.username_input = page.locator("[id='username']")
        self.password_input = page.locator("[id='password']")
        self.password_confirm_input = page.locator("[id='passwordSubmit']")
        self.submit_button = page.locator("[type='submit']")
        self.sign_in_form = page.locator("[class='form_sign-in']")
        self.error_message = page.locator("[class='form__error']")

    def click_register_link(self):
        with allure.step('Нажать "Create new account" для создания нового аккаунта'):
            self.register_link.click()

    def go_to_registration_form(self):
        with allure.step('Открыть форму регистрации'):
            self.click_register_link()
            self.wait_for_load()

    def fill_username(self, username: str):
        with allure.step('Заполнить логин'):
            self.username_input.fill(username)

    def fill_password(self, password: str):
        with allure.step('Заполнить пароль'):
            self.password_input.fill(password)

    def fill_password_confirmation(self, password: str):
        with allure.step('Подтвердить пароль'):
            self.password_confirm_input.fill(password)

    def click_submit(self):
        with allure.step('Нажать на кнопку submit'):
            self.submit_button.click()
            self.wait_for_load()

    def register(self, username: str, password: str, confirm_password: str = None):
        self.fill_username(username)
        self.fill_password(password)
        self.fill_password_confirmation(confirm_password or password)
        self.click_submit()

    def register_new_user(self):
        with allure.step('Зарегистрировать нового пользователя'):
            username = self.faker.user_name()
            password = self.faker.password()
            self.register(username, password)
            return username, password