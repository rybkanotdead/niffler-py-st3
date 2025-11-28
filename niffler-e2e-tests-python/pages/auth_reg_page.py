import os
from selene import browser, by, have


class AuthRegistrationPage:

    def __init__(self):
        self.username = browser.element('input[name=username]')
        self.password = browser.element('input[name=password]')
        self.pass_submit = browser.element('#passwordSubmit')
        self.login_btn = browser.element('.form__submit')
        self.register_btn = browser.element('.form__submit')

        self.to_register_btn = browser.element('.form__register')
        self.to_login_btn = browser.element('.form__link')
        self.eye_pass_btn = browser.element('#passwordBtn')
        self.eye_submit_pass_btn = browser.element('#passwordSubmitBtn')
        self.success_text = browser.element('p[class*=form__paragraph_success]')
        self.form_error = browser.element('.form__error')
        self.forms_error = browser.all('.form__error')

    def open_auth_page(self):
        return browser.open('/login')

    def open_register_page(self):
        return browser.open('/register')

    def fill_username(self, username: str):
        return self.username.type(username)

    def fill_password(self, password: str):
        return self.password.type(password)

    def submit_password(self, password: str):
        return self.pass_submit.type(password)

    def click_sign_up_btn(self):
        return self.register_btn.click()

    def to_login_form(self):
        return self.to_login_btn.click()

    def click_on_pass_eye(self):
        return self.eye_pass_btn.click()

    def click_on_submit_eye(self):
        return self.eye_submit_pass_btn.click()

    def login(self):
        self.open_auth_page()
        user = os.getenv('TEST_USERNAME')
        pwd = os.getenv('TEST_PASSWORD')
        if user and pwd:
            self.fill_username(user)
            self.fill_password(pwd)
            self.login_btn.click()