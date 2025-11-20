import time

from selene import be, have
from pages.auth_reg_page import AuthRegistrationPage
from pages.spendings_page import SpendingPage
from faker import Faker

auth_page = AuthRegistrationPage()
spending_page = SpendingPage()
faker = Faker()

class TestAuthPage:

    def test_login(self, existed_user_credentials):
        auth_page.open_auth_page()
        auth_page.fill_username(username=existed_user_credentials.get('username'))
        auth_page.fill_password(password=existed_user_credentials.get('password'))
        auth_page.click_sign_up_btn()
        spending_page.stat_area.should(be.visible)


    def test_logout(self):
        auth_page.login()
        spending_page.avatar_btn.click()
        time.sleep(3)
        spending_page.sign_out_btn.click()
        spending_page.logout_btn.click()
        auth_page.to_register_btn.should(be.visible)


    def test_login_invalid_creds(self):
        auth_page.open_auth_page()
        auth_page.fill_username(username=faker.user_name())
        auth_page.fill_password(password=faker.password())
        auth_page.login_btn.click()
        auth_page.form_error.should(be.visible)