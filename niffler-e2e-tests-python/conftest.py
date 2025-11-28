import os
import time
import pytest
from dotenv import load_dotenv
from selene import browser, have, be
from selenium.webdriver import ChromeOptions
from faker import Faker

from helpers.db_client import DBClient
from pages.auth_reg_page import AuthRegistrationPage
from pages.profile_page import ProfilePage
from pages.spendings_page import SpendingPage

load_dotenv()
faker = Faker()


@pytest.fixture(scope='session')
def envs():
    """Считываем переменные, включая настройку HEADLESS"""
    return {
        'auth_url': os.getenv('AUTH_URL'),
        'frontend_url': os.getenv('FRONTEND_URL'),
        'profile_url': os.getenv('PROFILE_URL'),
        'test_username': os.getenv('TEST_USERNAME'),
        'test_password': os.getenv('TEST_PASSWORD'),
        'pghost': os.getenv('PGHOST'),
        'pgport': os.getenv('PGPORT'),
        # Считываем HEADLESS. Если в файле написано true, вернет Python-булево True
        'headless': os.getenv('HEADLESS', 'false').lower() == 'true'
    }


@pytest.fixture(scope='session')
def app_url(envs):
    return envs['auth_url']


@pytest.fixture(scope='session')
def existed_user_credentials(envs):
    return {
        'username': envs['test_username'],
        'password': envs['test_password'],
    }


@pytest.fixture(scope='session')
def db():
    client = DBClient()
    yield client
    client.close()


@pytest.fixture(scope='function', autouse=True)
def browser_setup(app_url, envs):
    options = ChromeOptions()

    # === ЛОГИКА HEADLESS ===
    if envs['headless']:
        options.add_argument('--headless=new')

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')

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
    browser.config.timeout = 10.0

    yield
    browser.quit()


@pytest.fixture(scope='function')
def auth_page():
    return AuthRegistrationPage()


@pytest.fixture(scope='function')
def spending_page():
    return SpendingPage()


@pytest.fixture(scope='function')
def category(request):
    return request.param


@pytest.fixture(scope='function')
def login_user(auth_page, existed_user_credentials):
    """Логинимся и ждем"""
    auth_page.open_auth_page()
    auth_page.fill_username(existed_user_credentials['username'])
    auth_page.fill_password(existed_user_credentials['password'])
    auth_page.click_sign_up_btn()

    # Пауза для обработки логина сервером
    time.sleep(2)

    return auth_page


@pytest.fixture(scope='function')
def profile_page(login_user, envs):
    """Переходим в профиль по прямой ссылке"""
    browser.open(envs['profile_url'])
    return ProfilePage()


@pytest.fixture(scope='function')
def generate_user_data():
    return {
        'username': faker.user_name(),
        'password': faker.password(length=8),
        'submit_pass': faker.password(length=8),
    }


@pytest.fixture(scope='function')
def cleanup_spendings(spending_page):
    yield
    try:
        if spending_page.table_checkbox.is_displayed():
            spending_page.table_checkbox.click()
            spending_page.table_delete_btn.click()
            spending_page.delete_button.click()
            spending_page.delete_alert.click()
    except Exception:
        pass