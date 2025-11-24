import time
from selene import be, have
from faker import Faker

faker = Faker()

class TestAuthPage:


    def test_login(self, auth_page, spending_page, existed_user_credentials):
        auth_page.open_auth_page()
        auth_page.fill_username(username=existed_user_credentials.get('username'))
        auth_page.fill_password(password=existed_user_credentials.get('password'))
        auth_page.click_sign_up_btn()
        spending_page.stat_area.should(be.visible)

    def test_logout(self, auth_page, spending_page):
        auth_page.login()
        spending_page.avatar_btn.click()
        time.sleep(1)
        spending_page.sign_out_btn.click()
        spending_page.logout_btn.click()
        auth_page.to_register_btn.should(be.visible)

    def test_login_invalid_creds(self, auth_page):
        auth_page.open_auth_page()
        auth_page.fill_username(username=faker.user_name())
        auth_page.fill_password(password=faker.password())
        auth_page.login_btn.click()
        auth_page.form_error.should(be.visible)


    def test_login_empty_fields(self, auth_page):
        """Негативный тест: логин с пустыми полями"""
        auth_page.open_auth_page()
        auth_page.login_btn.click()
        auth_page.login_btn.should(be.visible)

    def test_switch_between_login_and_register(self, auth_page):
        """UI тест: переключение между формами"""
        auth_page.open_auth_page()
        auth_page.to_register_btn.click()
        auth_page.register_btn.should(have.text("Sign Up"))
        auth_page.to_login_btn.click()
        auth_page.login_btn.should(have.text("Log in"))