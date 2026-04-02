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
    @allure.title("Простой assert тест")
    def test_simple_assert(self):
        """Простой тест без зависимостей."""
        result = 5 + 5
        with allure.step(f"Проверяем что 5 + 5 = {result}"):
            assert result == 10, f"Expected 10 but got {result}"

    @pytest.mark.parametrize("value", [1, 2, 3, 4, 5])
    @allure.feature("smoke")
    @allure.story("parametrized")
    @allure.title("Параметризованные тесты")
    def test_parametrized(self, value):
        """Тест с параметризацией для демонстрации разнообразия."""
        with allure.step(f"Проверяем что {value} > 0"):
            assert value > 0, f"Значение {value} должно быть положительным"

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

    @allure.feature("smoke")
    @allure.story("infrastructure")
    @allure.title("Тест с множественными шагами")
    def test_multiple_steps(self):
        """Тест с множеством шагов для демонстрации."""
        with allure.step("Шаг 1: Инициализация"):
            value = 0
            assert value == 0

        with allure.step("Шаг 2: Инкремент"):
            value += 1
            assert value == 1

        with allure.step("Шаг 3: Удвоение"):
            value *= 2
            assert value == 2

        with allure.step("Шаг 4: Финальная проверка"):
            assert value == 2, f"Expected 2 but got {value}"

    @allure.feature("smoke")
    @allure.story("infrastructure")
    @allure.title("Тест со строковыми операциями")
    def test_string_operations(self):
        """Тест проверяет строковые операции."""
        with allure.step("Проверяем конкатенацию"):
            result = "Hello" + " " + "World"
            assert result == "Hello World"

        with allure.step("Проверяем длину строки"):
            assert len(result) == 11

        with allure.step("Проверяем наличие подстроки"):
            assert "World" in result

    @allure.feature("smoke")
    @allure.story("infrastructure")
    @allure.title("Тест с логированием в Allure")
    def test_with_logging(self):
        """Тест с логированием в Allure отчет."""
        with allure.step("Логируем информацию"):
            allure.attach(
                "Тестовое окружение запущено\n"
                "GitHub Actions: ✅\n"
                "Allure: ✅\n"
                "Workflow: ✅",
                name="test_environment",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Проверяем что логирование работает"):
            assert True



