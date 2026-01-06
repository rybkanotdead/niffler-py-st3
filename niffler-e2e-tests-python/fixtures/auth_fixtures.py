import pytest
from clients.auth_client import OAuthClient
from modals.config import Envs


@pytest.fixture(scope="session")
def auth_token(envs: Envs):
    return OAuthClient(envs).get_token(envs.niffler_username, envs.niffler_password)