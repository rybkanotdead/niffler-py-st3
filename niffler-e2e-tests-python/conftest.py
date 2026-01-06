import os
import time
import pytest
import allure
import requests
from urllib.parse import urljoin
from allure_commons.reporter import AllureReporter
from allure_pytest.listener import AllureListener
from pytest import FixtureDef, FixtureRequest
from dotenv import load_dotenv
from selene import browser
from selenium.webdriver.chrome.options import Options
from faker import Faker

# --- IMPORTS ИЗ ТВОЕГО ПРОЕКТА ---
from helpers.db_client import DBClient
from pages.auth_reg_page import AuthRegistrationPage
from pages.profile_page import ProfilePage
from pages.spendings_page import SpendingPage

# Импортируем API клиент из первого файла (проверь путь к файлу)
# Например, если файл называется clients/spends_client.py:
from clients.spends_client import SpendsHttpClient

load_dotenv()
faker = Faker()


def pytest_addoption(parser):
    """
    Добавляем опцию командной строки --headless.
    Теперь можно запускать так: poetry run pytest --headless
    """
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запуск тестов в режиме headless (без окна браузера)"
    )


def allure_reporter(config) -> AllureReporter:
    """Helper для получения репортера Allure"""
    listener: AllureListener = next(
        filter(
            lambda plugin: (isinstance(plugin, AllureListener)),
            dict(config.pluginmanager.list_name_plugin()).values(),
        ),
        None,
    )
    return listener.allure_logger


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_fixture_setup(fixturedef: FixtureDef, request: FixtureRequest):
    """
    Хук: Добавляет красивые имена фикстурам в отчет.
    """
    yield
    logger = allure_reporter(request.config)
    item = logger.get_last_item()
    if item:
        scope_letter = fixturedef.scope[0].upper()
        item.name = f"[{scope_letter}] " + " ".join(fixturedef.argname.split("_")).title()


def pytest_collection_modifyitems(items):
    """
    Хук: Убирает теги 'usefixtures' из отчета Allure.
    """
    for item in items:
        item.own_markers = [m for m in item.own_markers if m.name != 'usefixtures']


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук: При падении UI теста делает скриншот и прикладывает его в Allure.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == 'call' and rep.failed:
        try:
            # Проверяем, что драйвер существует и жив
            if hasattr(browser, 'driver') and browser.driver.session_id:
                allure.attach(
                    browser.driver.get_screenshot_as_png(),
                    name='Screenshot',
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(
                    browser.driver.page_source,
                    name='Page Source',
                    attachment_type=allure.attachment_type.HTML
                )
        except Exception as e:
            print(f"Browser is dead, cannot take screenshot: {e}")


# ==========================================
# CONFIG FIXTURES
# ==========================================

@allure.title("Загрузка переменных окружения")
@pytest.fixture(scope='session')
def envs():
    """Считываем переменные"""
    return {
        'auth_url': os.getenv('AUTH_URL'),
        'frontend_url': os.getenv('FRONTEND_URL'),
        'profile_url': os.getenv('PROFILE_URL'),
        'test_username': os.getenv('TEST_USERNAME'),
        'test_password': os.getenv('TEST_PASSWORD'),
        'pghost': os.getenv('PGHOST'),
        'pgport': os.getenv('PGPORT'),
        'headless': os.getenv('HEADLESS', 'false').lower() == 'true'
    }


@allure.title("Базовый URL приложения")
@pytest.fixture(scope='session')
def app_url(envs):
    return envs['auth_url']


@allure.title("Данные существующего пользователя")
@pytest.fixture(scope='session')
def existed_user_credentials(envs):
    return {
        'username': envs['test_username'],
        'password': envs['test_password'],
    }


@allure.title("Клиент базы данных")
@pytest.fixture(scope='session')
def db():
    client = DBClient()
    yield client
    client.close()


# ==========================================
# API FIXTURES (Новый блок)
# ==========================================

@allure.title("Получение токена авторизации (API)")
@pytest.fixture(scope='session')
def user_token(envs, existed_user_credentials):
    """
    Авторизуется через API, чтобы получить токен для SpendsHttpClient.
    Использует requests напрямую, чтобы не зависеть от UI.
    """
    # Предполагаемый эндпоинт логина. Если у тебя он другой, поправь путь.
    auth_endpoint = "/api/auth/login"
    url = urljoin(envs['auth_url'], auth_endpoint)

    with allure.step(f"Auth Setup: Получение токена для {existed_user_credentials['username']}"):
        response = requests.post(url, json=existed_user_credentials)
        response.raise_for_status()

        # Предполагаем, что токен лежит в ключе 'accessToken' или 'token'
        data = response.json()
        token = data.get('accessToken') or data.get('token')

        if not token:
            raise ValueError("Не удалось получить токен из ответа авторизации")

        return token


@allure.title("API клиент расходов")
@pytest.fixture(scope='function')
def api_spends(envs, user_token):
    """
    Возвращает готовый к использованию экземпляр SpendsHttpClient
    с настроенным URL и авторизацией.
    """
    client = SpendsHttpClient(base_url=envs['auth_url'], token=user_token)
    return client


# ==========================================
# UI FIXTURES
# ==========================================

@allure.title("Настройка браузера")
@pytest.fixture(scope='function', autouse=True)
def browser_setup(app_url, envs, request):
    options = Options()

    if envs['headless'] or request.config.getoption("--headless"):
        options.add_argument('--headless=new')

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
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


@allure.title("Страница авторизации")
@pytest.fixture(scope='function')
def auth_page():
    return AuthRegistrationPage()


@allure.title("Страница расходов")
@pytest.fixture(scope='function')
def spending_page():
    return SpendingPage()


@allure.title("Параметризация категории")
@pytest.fixture(scope='function')
def category(request):
    return request.param


@allure.title("Авторизация пользователя (UI)")
@pytest.fixture(scope='function')
def login_user(auth_page, existed_user_credentials):
    """Логинимся через браузер и ждем"""
    with allure.step("Открыть страницу авторизации и ввести данные"):
        auth_page.open_auth_page()
        auth_page.fill_username(existed_user_credentials['username'])
        auth_page.fill_password(existed_user_credentials['password'])
        auth_page.click_sign_up_btn()

    with allure.step("Ожидание обработки логина"):
        time.sleep(2)

    return auth_page


@allure.title("Страница профиля")
@pytest.fixture(scope='function')
def profile_page(login_user, envs):
    """Переходим в профиль по прямой ссылке"""
    with allure.step("Переход на страницу профиля"):
        browser.open(envs['profile_url'])
    return ProfilePage()


@allure.title("Генерация тестовых данных пользователя")
@pytest.fixture(scope='function')
def generate_user_data():
    return {
        'username': faker.user_name(),
        'password': faker.password(length=8),
        'submit_pass': faker.password(length=8),
    }


@allure.title("Очистка созданных трат")
@pytest.fixture(scope='function')
def cleanup_spendings(spending_page):
    yield
    with allure.step("Post-condition: Удаление траты"):
        try:
            if spending_page.table_checkbox.is_displayed():
                spending_page.table_checkbox.click()
                spending_page.table_delete_btn.click()
                spending_page.delete_button.click()
                spending_page.delete_alert.click()
        except Exception:
            pass