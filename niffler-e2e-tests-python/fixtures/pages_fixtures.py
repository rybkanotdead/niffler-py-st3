import pytest
from playwright.sync_api import Page
from pages.auth_page import LoginPage
from pages.profile_page import ProfilePage
from pages.registration_page import RegistrationPage
from pages.spendings_page import SpendingPage


@pytest.fixture()
def login_page(page: Page) -> LoginPage:
    login_page = LoginPage(page)
    return login_page


@pytest.fixture()
def open_login_page(login_page, envs):
    login_page.go_to(envs.auth_url)
    login_page.wait_for_load()


@pytest.fixture(scope="function")
def registration_page(page: Page, envs) -> RegistrationPage:
    registration_page = RegistrationPage(page, envs.auth_url)
    return registration_page


@pytest.fixture(scope="function")
def spending_page(page_with_auth: Page, envs) -> SpendingPage:
    spending_page = SpendingPage(page_with_auth, envs.frontend_url)
    return spending_page


@pytest.fixture(scope="function")
def profile_page(page_with_auth: Page) -> ProfilePage:
    profile_page = ProfilePage(page_with_auth)
    return profile_page


@pytest.fixture()
def open_profile_page(profile_page, envs):
    profile_page.go_to(envs.frontend_url + '/profile')
    profile_page.wait_for_load()