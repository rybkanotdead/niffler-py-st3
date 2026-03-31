"""
gRPC клиент для работы с сервисом Niffler Currency.

Сервис предоставляет:
- GetAllCurrencies — получение списка всех валют и курсов
- CalculateRate — конвертация суммы из одной валюты в другую
"""
import grpc
from typing import List

from clients.grpc_stubs import niffler_currency_pb2, niffler_currency_pb2_grpc
from clients.grpc_stubs.niffler_currency_pb2 import (
    CurrencyResponse,
    CalculateRequest,
    CalculateResponse,
    CurrencyValues,
)


class CurrencyGrpcClient:
    """gRPC клиент для Niffler Currency сервиса."""

    def __init__(self, host: str, port: int):
        """
        Инициализация gRPC клиента.

        Args:
            host: хост gRPC сервера (например, 'localhost')
            port: порт gRPC сервера (например, 8092)
        """
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = niffler_currency_pb2_grpc.NifflerCurrencyServiceStub(self.channel)

    def get_all_currencies(self) -> CurrencyResponse:
        """
        Получение списка всех валют с курсами.

        Returns:
            CurrencyResponse с полем allCurrencies (список Currency)
        """
        from google.protobuf import empty_pb2
        return self.stub.GetAllCurrencies(empty_pb2.Empty())

    def calculate_rate(
            self,
            spend_currency: str,
            desired_currency: str,
            amount: float
    ) -> CalculateResponse:
        """
        Конвертация суммы из одной валюты в другую.

        Args:
            spend_currency: исходная валюта ("RUB", "USD", "EUR", "KZT")
            desired_currency: целевая валюта
            amount: сумма для конвертации

        Returns:
            CalculateResponse с полем calculatedAmount
        """
        currency_map = {
            "UNSPECIFIED": CurrencyValues.UNSPECIFIED,
            "RUB": CurrencyValues.RUB,
            "USD": CurrencyValues.USD,
            "EUR": CurrencyValues.EUR,
            "KZT": CurrencyValues.KZT,
        }

        request = CalculateRequest(
            spendCurrency=currency_map.get(spend_currency, CurrencyValues.UNSPECIFIED),
            desiredCurrency=currency_map.get(desired_currency, CurrencyValues.UNSPECIFIED),
            amount=amount,
        )
        return self.stub.CalculateRate(request)

    def close(self) -> None:
        """Закрытие gRPC канала."""
        self.channel.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

