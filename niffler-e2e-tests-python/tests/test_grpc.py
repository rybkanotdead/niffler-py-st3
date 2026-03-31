"""
gRPC тесты для Niffler Currency сервиса.

Тесты проверяют:
1. Получение списка всех валют через gRPC
2. Конвертацию курсов валют через gRPC
3. Корректность возвращаемых данных
"""
import pytest
import allure

from clients.grpc_client import CurrencyGrpcClient


@pytest.mark.grpc
@pytest.mark.smoke
class TestCurrencyGrpc:
    """gRPC тесты для Currency сервиса."""

    @allure.title("gRPC: получение списка всех валют")
    @allure.description(
        """
        Шаги:
        1. Отправляем gRPC запрос GetAllCurrencies
        2. Проверяем, что ответ содержит список валют
        3. Проверяем, что каждая валюта имеет курс > 0

        Ожидается: список содержит все 4 валюты (RUB, USD, EUR, KZT)
        """
    )
    @allure.feature("gRPC")
    @allure.story("Currency")
    def test_get_all_currencies(self, grpc_client: CurrencyGrpcClient):
        """Получение всех валют через gRPC."""
        with allure.step("Отправка gRPC запроса GetAllCurrencies"):
            response = grpc_client.get_all_currencies()

        with allure.step("Проверка наличия валют в ответе"):
            assert response is not None, "Ответ не должен быть None"
            assert len(response.allCurrencies) > 0, "Список валют не должен быть пустым"

        with allure.step("Проверка количества валют"):
            currency_names = [c.currency for c in response.allCurrencies]
            allure.attach(
                str([(c.currency, c.currencyRate) for c in response.allCurrencies]),
                name="currencies",
                attachment_type=allure.attachment_type.TEXT,
            )
            # CurrencyValues: 1=RUB, 2=USD, 3=EUR, 4=KZT
            assert len(response.allCurrencies) == 4, (
                f"Ожидается 4 валюты, получено: {len(response.allCurrencies)}"
            )

        with allure.step("Проверка корректности курсов"):
            for currency in response.allCurrencies:
                assert currency.currencyRate > 0, (
                    f"Курс валюты {currency.currency} должен быть > 0"
                )

    @allure.title("gRPC: конвертация суммы из RUB в USD")
    @allure.description(
        """
        Шаги:
        1. Отправляем gRPC запрос CalculateRate (RUB → USD, сумма 1000)
        2. Проверяем, что calculatedAmount > 0
        3. Проверяем разумность результата

        Ожидается: конвертация выполнена, возвращена корректная сумма
        """
    )
    @allure.feature("gRPC")
    @allure.story("Currency")
    def test_calculate_rate_rub_to_usd(self, grpc_client: CurrencyGrpcClient):
        """Конвертация RUB → USD через gRPC."""
        amount = 1000.0

        with allure.step(f"Конвертация {amount} RUB → USD"):
            response = grpc_client.calculate_rate(
                spend_currency="RUB",
                desired_currency="USD",
                amount=amount,
            )

        with allure.step("Проверка результата конвертации"):
            allure.attach(
                f"Исходная сумма: {amount} RUB\nКонвертировано: {response.calculatedAmount} USD",
                name="calculation_result",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert response.calculatedAmount > 0, (
                f"Конвертированная сумма должна быть > 0, получено: {response.calculatedAmount}"
            )
            # 1000 RUB < 1000 USD (разумная проверка)
            assert response.calculatedAmount < amount, (
                f"1000 RUB должно быть меньше 1000 USD"
            )

    @allure.title("gRPC: конвертация суммы из USD в RUB")
    @allure.feature("gRPC")
    @allure.story("Currency")
    def test_calculate_rate_usd_to_rub(self, grpc_client: CurrencyGrpcClient):
        """Конвертация USD → RUB через gRPC."""
        amount = 10.0

        with allure.step(f"Конвертация {amount} USD → RUB"):
            response = grpc_client.calculate_rate(
                spend_currency="USD",
                desired_currency="RUB",
                amount=amount,
            )

        with allure.step("Проверка результата конвертации"):
            allure.attach(
                f"Исходная сумма: {amount} USD\nКонвертировано: {response.calculatedAmount} RUB",
                name="calculation_result",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert response.calculatedAmount > 0, (
                f"Конвертированная сумма должна быть > 0"
            )
            # 10 USD > 10 RUB
            assert response.calculatedAmount > amount, (
                f"10 USD должно быть больше 10 RUB"
            )

    @allure.title("gRPC: конвертация одинаковых валют возвращает ту же сумму")
    @allure.feature("gRPC")
    @allure.story("Currency")
    def test_calculate_rate_same_currency(self, grpc_client: CurrencyGrpcClient):
        """Конвертация RUB → RUB должна вернуть ту же сумму."""
        amount = 500.0

        with allure.step(f"Конвертация {amount} RUB → RUB"):
            response = grpc_client.calculate_rate(
                spend_currency="RUB",
                desired_currency="RUB",
                amount=amount,
            )

        with allure.step("Проверка: сумма не изменилась"):
            assert response.calculatedAmount == pytest.approx(amount, rel=1e-3), (
                f"Конвертация одинаковых валют должна возвращать исходную сумму. "
                f"Ожидалось: {amount}, получено: {response.calculatedAmount}"
            )

    @allure.title("gRPC: конвертация EUR в KZT")
    @allure.feature("gRPC")
    @allure.story("Currency")
    def test_calculate_rate_eur_to_kzt(self, grpc_client: CurrencyGrpcClient):
        """Конвертация EUR → KZT через gRPC."""
        amount = 100.0

        with allure.step(f"Конвертация {amount} EUR → KZT"):
            response = grpc_client.calculate_rate(
                spend_currency="EUR",
                desired_currency="KZT",
                amount=amount,
            )

        with allure.step("Проверка результата"):
            assert response.calculatedAmount > 0
            # 100 EUR >> 100 KZT (евро дороже тенге)
            assert response.calculatedAmount > amount

