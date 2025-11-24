import os
import pytest
from dotenv import load_dotenv
from selene import browser
from selenium.webdriver import ChromeOptions
from faker import Faker
from pages.auth_reg_page import AuthRegistrationPage
from pages.spendings_page import SpendingPage

load_dotenv()
faker = Faker()


@pytest.fixture(scope='session')
def app_url():
    return os.getenv('AUTH_URL')


@pytest.fixture(scope='session')
def existed_user_credentials():
    return {
        'username': os.getenv('TEST_USERNAME'),
        'password': os.getenv('TEST_PASSWORD'),
    }


@pytest.fixture(scope='function', autouse=True)
def browser_setup(app_url):
    options = ChromeOptions()

    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    prefs = {
        "profile.password_manager_leak_detection": False,
        "credentials_enable_service": False,
        "password_manager_enabled": False
    }
    options.add_experimental_option('prefs', prefs)
    browser.config.driver_options = options
    browser.config.base_url = app_url
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    yield

    browser.quit()


# Остальные фикстуры (auth_page, spending_page, login_user и т.д.) оставляй без изменений
@pytest.fixture(scope='function')
def auth_page():
    return AuthRegistrationPage()


@pytest.fixture(scope='function')
def spending_page():
    return SpendingPage()


@pytest.fixture(scope='function')
def generate_user_data():
    return {
        'username': faker.user_name(),
        'password': faker.password(length=8),
        'submit_pass': faker.password(length=8),
    }


@pytest.fixture(scope='function')
def login_user(auth_page, existed_user_credentials):
    auth_page.open_auth_page()
    auth_page.fill_username(existed_user_credentials['username'])
    auth_page.fill_password(existed_user_credentials['password'])
    auth_page.click_sign_up_btn()
    return auth_page


@pytest.fixture(scope='function')
def cleanup_spendings(spending_page):
    yield
    try:
        if spending_page.table_checkbox.is_displayed():
            spending_page.table_checkbox.click()
            spending_page.table_delete_btn.click()
            spending_page.delete_button.click()
            spending_page.delete_alert.click()
    except:
        pass