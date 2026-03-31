"""
Конфигурация и константы приложения.
"""
from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv


@dataclass
class Config:
    """Конфигурация приложения."""

    # URLs
    auth_url: str
    frontend_url: str
    profile_url: str
    gateway_url: str

    # Database
    spend_db_url: str
    pghost: str
    pgport: str

    # Credentials
    test_username: str
    test_password: str

    # gRPC (Currency service)
    grpc_host: str = "localhost"
    grpc_port: int = 8092

    # SOAP (Userdata service)
    soap_url: str = "http://localhost:8089/ws"

    # Kafka
    kafka_bootstrap_servers: str = "localhost:9092"

    # Browser
    headless: bool = False
    browser_timeout: int = 10
    window_width: int = 1920
    window_height: int = 1080

    @classmethod
    def from_env(cls) -> 'Config':
        """Загрузка конфигурации из переменных окружения."""
        load_dotenv()

        return cls(
            auth_url=os.getenv('AUTH_URL', 'http://localhost:3000'),
            frontend_url=os.getenv('FRONTEND_URL', 'http://localhost:3000'),
            profile_url=os.getenv('PROFILE_URL', 'http://localhost:3000/profile'),
            gateway_url=os.getenv('GATEWAY_URL', 'http://localhost:8080'),
            spend_db_url=os.getenv('SPEND_DB_URL', 'postgresql://postgres:secret@localhost:5432/niffler-spend'),
            pghost=os.getenv('PGHOST', 'localhost'),
            pgport=os.getenv('PGPORT', '5432'),
            test_username=os.getenv('TEST_USERNAME', ''),
            test_password=os.getenv('TEST_PASSWORD', ''),
            grpc_host=os.getenv('GRPC_HOST', 'localhost'),
            grpc_port=int(os.getenv('GRPC_PORT', '8092')),
            soap_url=os.getenv('SOAP_URL', 'http://localhost:8089/ws'),
            kafka_bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
            headless=os.getenv('HEADLESS', 'false').lower() == 'true',
            browser_timeout=int(os.getenv('BROWSER_TIMEOUT', '10')),
        )


# Глобальная конфигурация (инициализируется один раз)
config: Optional[Config] = None


def get_config() -> Config:
    """Получение конфигурации (singleton)."""
    global config
    if config is None:
        config = Config.from_env()
    return config

