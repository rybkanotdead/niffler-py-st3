import os
import pytest
from dotenv import load_dotenv
from selene import browser
from selenium.webdriver import ChromeOptions
from faker import Faker


faker = Faker()
load_dotenv()


@pytest.fixture()
def app_url():
    return os.getenv('AUTH_URL')


@pytest.fixture()
def existed_user_credentials():
    return {
        'username': os.getenv('TEST_USERNAME'),
        'password': os.getenv('TEST_PASSWORD'),
    }


@pytest.fixture(scope='function', autouse=True)
def browser_setup(app_url):
    options = ChromeOptions()
    prefs = {
        "profile.password_manager_leak_detection": False,
    }
    options.add_experimental_option('prefs', prefs)
    browser.config.driver_options = options
    browser.config.base_url = app_url
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.open('/')
    yield
    browser.quit()


@pytest.fixture(scope='function')
def generate_user_data():
    return {
        'username': faker.user_name(),
        'password': faker.password(length=8),
        'submit_pass': faker.password(length=8),
    }