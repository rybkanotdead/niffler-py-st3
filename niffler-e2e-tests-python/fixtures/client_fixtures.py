import pytest
from clients.spends_client import SpendsHttpClient
from databases.spend_db import SpendDb
from modals.config import Envs


@pytest.fixture(scope="session")
def spends_client(envs: Envs, auth_token) -> SpendsHttpClient:
    return SpendsHttpClient(envs, auth_token)


@pytest.fixture(scope="session")
def spend_db(envs) -> SpendDb:
    return SpendDb(envs)