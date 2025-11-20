from selene import have, be
from pages.auth_reg_page import AuthRegistrationPage

page = AuthRegistrationPage()


class TestRegistration:

    def test_register_user(self, generate_user_data):
        page.open_auth_page()
        page.to_register_btn.click()
        page.fill_username(username=generate_user_data.get('username'))
        page.fill_password(password=generate_user_data.get('password'))
        page.click_on_pass_eye()
        page.eye_pass_btn.should(have.attribute('class', 'form__password-button form__password-button_active'))
        page.submit_password(password=generate_user_data.get('password'))
        page.click_on_submit_eye()
        page.eye_submit_pass_btn.should(have.attribute('class', 'form__password-button form__password-button_active'))
        page.click_sign_up_btn()
        page.success_text.should(have.text("Congratulations! You've registered!"))


    def test_register_existed_user(self, existed_user_credentials):
        page.open_register_page()
        page.fill_username(username=existed_user_credentials.get('username'))
        page.fill_password(password=existed_user_credentials.get('password'))
        page.submit_password(password=existed_user_credentials.get('password'))
        page.click_sign_up_btn()
        page.form_error.should(be.visible).should(
            have.text(f'Username `{existed_user_credentials.get("username")}` already exists'))


    def test_register_user_invalid_pass(self, generate_user_data):
        page.open_register_page()
        page.fill_username(username=generate_user_data.get('username'))
        page.fill_password(password=generate_user_data.get('password'))
        page.submit_password(password=generate_user_data.get('submit_pass'))
        page.click_sign_up_btn()
        page.form_error.should(be.visible).should(have.text('Passwords should be equal'))


    def test_visible_input_errors(self):
        page.open_register_page()
        page.fill_username(username='1')
        page.fill_password(password='1')
        page.submit_password(password='1')
        page.click_sign_up_btn()
        page.forms_error[0].should(have.text('Allowed username length should be from 3 to 50 characters')).should(
            be.visible
        )
        page.forms_error[1].should(have.text('Allowed password length should be from 3 to 12 characters')).should(
            be.visible
        )
        page.forms_error[2].should(have.text('Allowed password length should be from 3 to 12 characters')).should(
            be.visible
        )