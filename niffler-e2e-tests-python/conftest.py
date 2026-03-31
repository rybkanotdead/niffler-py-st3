"""
Конфигурация pytest и фикстуры для E2E тестов Niffler.
Организована по слоям: конфигурация, БД, браузер, страницы, авторизация, генерация данных, очистка.
"""
import time
from typing import Generator

import pytest
import allure
from selene import browser
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker

from config import get_config
from clients.api import CategoryApiClient, SpendApiClient
from clients.grpc_client import CurrencyGrpcClient
from clients.soap_client import UserdataSoapClient
from clients.kafka_client import KafkaClient
from helpers.db_client import DBClient
from pages.auth_reg_page import AuthRegistrationPage
from pages.profile_page import ProfilePage
from pages.spendings_page import SpendingPage

# ============================================================================
# ИНИЦИАЛИЗАЦИЯ
# ============================================================================

fake = Faker()


# ============================================================================
# SESSION SCOPE FIXTURES — конфигурация и сервисы (один раз на сессию)
# ============================================================================

@pytest.fixture(scope='session')
def config():
    """Загрузка конфигурации из .env."""
    cfg = get_config()
    with allure.step("Инициализация конфигурации"):
        allure.attach(
            f"Frontend: {cfg.frontend_url}\n"
            f"Gateway: {cfg.gateway_url}\n"
            f"DB: {cfg.pghost}:{cfg.pgport}",
            name="environment_config",
            attachment_type=allure.attachment_type.TEXT
        )
    return cfg


@pytest.fixture(scope='session')
def db(config) -> Generator[DBClient, None, None]:
    """Клиент PostgreSQL — один на сессию."""
    with allure.step("Подключение к БД"):
        client = DBClient(db_url=config.spend_db_url)
    yield client
    with allure.step("Закрытие подключения к БД"):
        client.close()


@pytest.fixture(scope='session')
def auth_token(config) -> str:
    """
    Получение JWT-токена через UI авторизацию.
    Использует отдельный экземпляр Selenium (не Selene-синглтон),
    чтобы не конфликтовать с function-scope browser_setup.
    Токен живёт на всю сессию — используется в API клиентах.
    """
    options = ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_experimental_option('prefs', {
        "credentials_enable_service": False,
        "password_manager_enabled": False,
    })

    driver = webdriver.Chrome(options=options)
    token = ""
    try:
        driver.get(f"{config.auth_url}/login")
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name=username]')))
        driver.find_element(By.CSS_SELECTOR, 'input[name=username]').send_keys(config.test_username)
        driver.find_element(By.CSS_SELECTOR, 'input[name=password]').send_keys(config.test_password)
        driver.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()
        # Ждём перехода на главную страницу
        wait.until(EC.presence_of_element_located((By.ID, 'spendings')))
        token = driver.execute_script('return window.localStorage.getItem("id_token")') or ""
        with allure.step("Токен авторизации получен"):
            allure.attach(
                f"Token length: {len(token)} chars",
                name="auth_token_info",
                attachment_type=allure.attachment_type.TEXT,
            )
    except Exception as e:
        allure.attach(str(e), name="auth_token_error", attachment_type=allure.attachment_type.TEXT)
    finally:
        driver.quit()

    return token


@pytest.fixture(scope='session')
def category_api_client(config, auth_token) -> Generator[CategoryApiClient, None, None]:
    """API клиент категорий (с реальным JWT-токеном)."""
    client = CategoryApiClient(config.gateway_url, auth_token)
    yield client
    client.close()


@pytest.fixture(scope='session')
def spend_api_client(config, auth_token) -> Generator[SpendApiClient, None, None]:
    """API клиент трат (с реальным JWT-токеном)."""
    client = SpendApiClient(config.gateway_url, auth_token)
    yield client
    client.close()


@pytest.fixture(scope='session')
def category_client(category_api_client) -> CategoryApiClient:
    """Алиас category_api_client для тестов."""
    return category_api_client


@pytest.fixture(scope='session')
def spends_client(spend_api_client) -> SpendApiClient:
    """Алиас spend_api_client для тестов."""
    return spend_api_client


@pytest.fixture(scope='session')
def grpc_client(config) -> Generator[CurrencyGrpcClient, None, None]:
    """gRPC клиент для Currency сервиса (порт 8092)."""
    client = CurrencyGrpcClient(host=config.grpc_host, port=config.grpc_port)
    yield client
    client.close()


@pytest.fixture(scope='session')
def soap_client(config) -> Generator[UserdataSoapClient, None, None]:
    """SOAP клиент для Userdata сервиса (порт 8089/ws)."""
    client = UserdataSoapClient(soap_url=config.soap_url)
    yield client
    client.close()


@pytest.fixture(scope='session')
def kafka_client(config) -> KafkaClient:
    """Kafka клиент для топика 'users'."""
    return KafkaClient(bootstrap_servers=config.kafka_bootstrap_servers)


# ============================================================================
# FUNCTION SCOPE — браузер
# ============================================================================

def _build_chrome_options(config) -> ChromeOptions:
    """Вспомогательная функция сборки опций Chrome."""
    options = ChromeOptions()
    if config.headless:
        options.add_argument('--headless=new')
    for arg in [
        '--no-sandbox',
        '--disable-dev-shm-usage',
        f'--window-size={config.window_width},{config.window_height}',
        '--disable-gpu',
        '--start-maximized',
    ]:
        options.add_argument(arg)
    options.add_experimental_option('prefs', {
        "profile.password_manager_leak_detection": False,
        "credentials_enable_service": False,
        "password_manager_enabled": False,
    })
    return options


@pytest.fixture(scope='function')
def browser_setup(config) -> Generator[None, None, None]:
    """
    Инициализация браузера (Selene) перед UI тестом.
    НЕ autouse — запускается только для тестов, использующих auth_page/spending_page.
    """
    browser.config.driver_options = _build_chrome_options(config)
    browser.config.base_url = config.auth_url
    browser.config.window_width = config.window_width
    browser.config.window_height = config.window_height
    browser.config.timeout = config.browser_timeout

    yield

    if hasattr(pytest, 'last_test_failed') and pytest.last_test_failed:
        try:
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception:
            pass

    browser.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для определения статуса теста (для скриншотов)."""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        pytest.last_test_failed = rep.failed


# ============================================================================
# FUNCTION SCOPE — учётные данные
# ============================================================================

@pytest.fixture(scope='function')
def existed_user_credentials(config) -> dict:
    """Учётные данные существующего тестового пользователя."""
    return {
        'username': config.test_username,
        'password': config.test_password,
    }


# ============================================================================
# FUNCTION SCOPE — Page Objects
# Каждый page object явно зависит от browser_setup,
# поэтому Chrome запускается только для UI-тестов.
# ============================================================================

@pytest.fixture(scope='function')
def auth_page(browser_setup) -> AuthRegistrationPage:
    """Page Object авторизации / регистрации."""
    return AuthRegistrationPage()


@pytest.fixture(scope='function')
def spending_page(browser_setup) -> SpendingPage:
    """Page Object страницы трат."""
    return SpendingPage()


@pytest.fixture(scope='function')
def profile_page(login_user, config) -> ProfilePage:
    """Page Object профиля (требует авторизации)."""
    with allure.step(f"Открытие профиля: {config.profile_url}"):
        browser.open(config.profile_url)
    return ProfilePage()


@pytest.fixture(scope='function')
def main_page(login_user, config):
    """Главная страница (требует авторизации)."""
    browser.open(config.frontend_url)


# ============================================================================
# FUNCTION SCOPE — авторизация
# ============================================================================

@pytest.fixture(scope='function')
def login_user(auth_page: AuthRegistrationPage, existed_user_credentials: dict):
    """Авторизация пользователя через UI."""
    with allure.step(f"Авторизация: {existed_user_credentials['username']}"):
        auth_page.open_auth_page()
        auth_page.fill_username(existed_user_credentials['username'])
        auth_page.fill_password(existed_user_credentials['password'])
        auth_page.click_sign_up_btn()
        time.sleep(2)
    return auth_page


# ============================================================================
# FUNCTION SCOPE — генерация тестовых данных
# ============================================================================

@pytest.fixture(scope='function')
def random_category_name() -> str:
    """Случайное имя категории."""
    return f"cat_{fake.word()}_{fake.bothify(text='####')}"


@pytest.fixture(scope='function')
def generate_user_data() -> dict:
    """Случайные данные для нового пользователя.
    submit_pass содержит неверный пароль — используется в тестах на несовпадение паролей.
    Для тестов регистрации с совпадающими паролями используйте 'password' дважды.
    """
    password = fake.password(length=8, special_chars=False)
    return {
        'username': fake.user_name() + '_' + fake.bothify(text='####'),
        'password': password,
        'submit_pass': password + '_wrong',
    }


# ============================================================================
# FUNCTION SCOPE — очистка (teardown)
# ============================================================================

@pytest.fixture(scope='function')
def cleanup_categories(db: DBClient) -> Generator[list, None, None]:
    """Очистка категорий из БД после теста. Принимает список ID для удаления."""
    ids: list[str] = []
    yield ids
    with allure.step("Очистка: удаление категорий из БД"):
        for cat_id in ids:
            try:
                db.delete_category_by_id(cat_id)
            except Exception as e:
                allure.attach(str(e), name="cleanup_error", attachment_type=allure.attachment_type.TEXT)


@pytest.fixture(scope='function')
def cleanup_db_spends(db: DBClient) -> Generator[list, None, None]:
    """Очистка трат из БД после теста. Принимает список ID для удаления."""
    ids: list[str] = []
    yield ids
    with allure.step("Очистка: удаление трат из БД"):
        for spend_id in ids:
            try:
                db.delete_spend(spend_id)
            except Exception as e:
                allure.attach(str(e), name="cleanup_error", attachment_type=allure.attachment_type.TEXT)


@pytest.fixture(scope='function')
def cleanup_spendings(spending_page: SpendingPage) -> Generator[None, None, None]:
    """Очистка трат через UI после теста."""
    yield
    with allure.step("Очистка: удаление трат через UI"):
        try:
            if spending_page.table_checkbox.is_displayed():
                spending_page.table_checkbox.click()
                spending_page.table_delete_btn.click()
                spending_page.delete_button.click()
        except Exception:
            pass


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

def pytest_configure(config):
    """Регистрация кастомных маркеров."""
    for marker in [
        "ui: UI тесты (Selenium/Selene)",
        "api: API тесты (requests)",
        "db: Тесты интеграции с БД",
        "grpc: gRPC тесты (Currency сервис)",
        "soap: SOAP тесты (Userdata сервис)",
        "kafka: Kafka тесты (топик users)",
        "smoke: Smoke тесты",
        "regression: Регрессионные тесты",
        "integration: Интеграционные тесты",
    ]:
        config.addinivalue_line("markers", marker)

