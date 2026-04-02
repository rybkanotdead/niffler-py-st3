"""
Простой conftest.py для tests/ папки.
Полностью независимый от родительского conftest.py.
Обеспечивает что smoke тесты могут запуститься в любом окружении.
"""
import sys
from pathlib import Path

# Добавляем родительскую директорию в path для относительных импортов
tests_dir = Path(__file__).parent
parent_dir = tests_dir.parent
sys.path.insert(0, str(parent_dir))

import pytest
import allure


# ============================================================================
# БАЗОВЫЕ ФИКСТУРЫ
# ============================================================================

@pytest.fixture(scope='session')
def config():
    """Минимальная конфигурация для тестов."""
    class Config:
        frontend_url = "http://localhost:3000"
        auth_url = "http://localhost:9000"
        gateway_url = "http://localhost:8080"
        grpc_host = "localhost"
        grpc_port = 8092
        soap_url = "http://localhost:8089/ws"
        kafka_bootstrap_servers = "localhost:9092"
    
    return Config()


@pytest.fixture(scope='session')
def _services():
    """Статус сервисов - в GitHub Actions все будут недоступны."""
    return {
        'auth': False,
        'frontend': False,
        'gateway': False,
        'grpc': False,
        'soap': False,
        'kafka': False,
    }


# ============================================================================
# АВТОМАТИЧЕСКИЕ SKIP'ы
# ============================================================================

@pytest.fixture(scope='function', autouse=True)
def _auto_skip(request, _services):
    """
    Автоматически пропускает тесты которые требуют недоступных сервисов.
    Smoke тесты будут работать потому что они не используют эти фикстуры.
    """
    markers = {m.name for m in request.node.iter_markers()}
    fixtures = set(request.fixturenames)

    # Пропускаем тесты UI если фикстуры UI требуются но frontend недоступен
    ui_fixtures = {'auth_page', 'spending_page', 'profile_page', 'login_user',
                   'browser_setup', 'auth_token'}
    
    if fixtures & ui_fixtures and not _services['frontend']:
        pytest.skip("⏭ Frontend сервис недоступен")

    if 'grpc' in markers and not _services['grpc']:
        pytest.skip("⏭ gRPC сервис недоступен")

    if 'soap' in markers and not _services['soap']:
        pytest.skip("⏭ SOAP сервис недоступен")

    if 'kafka' in markers and not _services['kafka']:
        pytest.skip("⏭ Kafka сервис недоступен")
