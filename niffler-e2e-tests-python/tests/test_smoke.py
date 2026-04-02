"""
Smoke тесты для проверки что Allure отчет работает.
Эти тесты НЕ требуют запущенных сервисов и всегда будут запущены.
"""
import pytest
import allure


class TestSmoke:
    """Дымовые тесты для базовой проверки инфраструктуры."""

    @allure.feature("smoke")
    @allure.story("infrastructure")
    @allure.title("Проверка работы Allure отчета")
    def test_allure_report_works(self):
        """Базовый тест для проверки что Allure отчет генерируется."""
        with allure.step("Шаг 1: Проверяем что тест работает"):
            assert True, "Тест успешно прошел"

        with allure.step("Шаг 2: Проверяем Allure аннотации"):
            assert 1 + 1 == 2, "Математика работает"

    @allure.feature("smoke")
    @allure.story("infrastructure")
    @allure.title("Тест конфигурации")
    def test_config_loaded(self, config):
        """Проверяем что конфигурация загружена."""
        with allure.step("Проверяем наличие основных параметров конфигурации"):
            assert config.frontend_url, "Frontend URL должен быть установлен"
            assert config.auth_url, "Auth URL должен быть установлен"
            assert config.gateway_url, "Gateway URL должен быть установлен"

    @allure.feature("smoke")
    @allure.story("infrastructure")
    @allure.title("Проверка доступности сервисов")
    def test_services_status(self, _services):
        """Информационный тест - выводит статус доступности сервисов."""
        with allure.step("Статус сервисов"):
            for service, status in _services.items():
                service_status = "✅ доступен" if status else "⏭ пропущен (не доступен)"
                allure.attach(
                    f"{service}: {service_status}",
                    name=f"service_{service}",
                    attachment_type=allure.attachment_type.TEXT
                )
        # Тест всегда проходит - это информационный тест
        assert True

    @pytest.mark.parametrize("test_num", range(1, 4))
    @allure.feature("smoke")
    @allure.story("parametrized")
    @allure.title("Параметризованные тесты")
    def test_parametrized(self, test_num):
        """Тест с параметризацией для демонстрации разнообразия."""
        with allure.step(f"Проверяем параметр {test_num}"):
            assert test_num > 0, f"Параметр {test_num} должен быть положительным"

    @allure.feature("smoke")
    @allure.story("infrastructure")
    @allure.title("Демо тест с attachments")
    def test_with_attachments(self):
        """Тест демонстрирует работу attachments в Allure."""
        with allure.step("Добавляем текстовый attachment"):
            allure.attach(
                "Это демо текстовый attachment\nОн будет виден в Allure отчете",
                name="demo_text",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Добавляем JSON attachment"):
            import json
            data = {
                "project": "niffler-py",
                "report": "allure",
                "status": "working"
            }
            allure.attach(
                json.dumps(data, indent=2),
                name="config_data",
                attachment_type=allure.attachment_type.JSON
            )

        assert True

