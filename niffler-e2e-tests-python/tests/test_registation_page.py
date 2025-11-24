from selene import have, be

class TestRegistration:


    def test_register_user(self, auth_page, generate_user_data):
        auth_page.open_auth_page()
        auth_page.to_register_btn.click()
        auth_page.fill_username(username=generate_user_data.get('username'))
        auth_page.fill_password(password=generate_user_data.get('password'))
        auth_page.click_on_pass_eye()
        auth_page.eye_pass_btn.should(have.attribute('class', 'form__password-button form__password-button_active'))
        auth_page.submit_password(password=generate_user_data.get('password'))
        auth_page.click_on_submit_eye()
        auth_page.eye_submit_pass_btn.should(have.attribute('class', 'form__password-button form__password-button_active'))
        auth_page.click_sign_up_btn()
        auth_page.success_text.should(have.text("Congratulations! You've registered!"))

    def test_register_existed_user(self, auth_page, existed_user_credentials):
        auth_page.open_register_page()
        auth_page.fill_username(username=existed_user_credentials.get('username'))
        auth_page.fill_password(password=existed_user_credentials.get('password'))
        auth_page.submit_password(password=existed_user_credentials.get('password'))
        auth_page.click_sign_up_btn()
        auth_page.form_error.should(be.visible).should(
            have.text(f'Username `{existed_user_credentials.get("username")}` already exists'))

    def test_register_user_invalid_pass(self, auth_page, generate_user_data):
        auth_page.open_register_page()
        auth_page.fill_username(username=generate_user_data.get('username'))
        auth_page.fill_password(password=generate_user_data.get('password'))
        auth_page.submit_password(password=generate_user_data.get('submit_pass'))
        auth_page.click_sign_up_btn()
        auth_page.form_error.should(be.visible).should(have.text('Passwords should be equal'))

    def test_visible_input_errors(self, auth_page):
        auth_page.open_register_page()
        auth_page.fill_username(username='1')
        auth_page.fill_password(password='1')
        auth_page.submit_password(password='1')
        auth_page.click_sign_up_btn()
        auth_page.forms_error[0].should(have.text('Allowed username length should be from 3 to 50 characters')).should(
            be.visible
        )
        auth_page.forms_error[1].should(have.text('Allowed password length should be from 3 to 12 characters')).should(
            be.visible
        )
        auth_page.forms_error[2].should(have.text('Allowed password length should be from 3 to 12 characters')).should(
            be.visible
        )


    def test_register_short_password(self, auth_page, generate_user_data):
        """Негативный тест: пароль короче 3 символов"""
        auth_page.open_register_page()
        auth_page.fill_username(generate_user_data['username'])
        short_pass = "12"
        auth_page.fill_password(short_pass)
        auth_page.submit_password(short_pass)
        auth_page.click_sign_up_btn()
        auth_page.forms_error[1].should(have.text('Allowed password length should be from 3 to 12 characters'))

    def test_register_empty_fields(self, auth_page):
        """Негативный тест: попытка регистрации с пустыми полями"""
        auth_page.open_register_page()
        auth_page.click_sign_up_btn()
        auth_page.register_btn.should(be.visible)