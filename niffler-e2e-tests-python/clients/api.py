"""
HTTP клиенты для работы с REST API Niffler.
"""
from typing import Optional, List
from urllib.parse import urljoin
import requests


class BaseHttpClient:
    """Базовый класс для HTTP клиентов."""

    def __init__(self, base_url: str, token: str):
        """
        Инициализация HTTP клиента.
        
        Args:
            base_url: Base URL API
            token: Bearer token для авторизации
        """
        self.base_url = base_url
        self.session = requests.Session()
        self._set_auth_headers(token)

    def _set_auth_headers(self, token: str) -> None:
        """Установка заголовков авторизации."""
        self.session.headers.update({
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        })

    def _build_url(self, path: str) -> str:
        """Построение полного URL."""
        return urljoin(self.base_url, path)

    def _raise_for_status(self, response: requests.Response) -> None:
        """Обработка ошибок HTTP."""
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == 400:
                e.add_note(response.text)
            raise

    def close(self) -> None:
        """Закрытие сессии."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class CategoryApiClient(BaseHttpClient):
    """HTTP клиент для работы с категориями."""

    def add_category(self, name: str) -> dict:
        """Создание категории."""
        url = self._build_url("/api/categories/add")
        payload = {"name": name}
        response = self.session.post(url, json=payload)
        self._raise_for_status(response)
        return response.json()

    def get_categories(self) -> List[dict]:
        """Получение всех категорий."""
        url = self._build_url("/api/categories/all")
        response = self.session.get(url)
        self._raise_for_status(response)
        return response.json()

    def edit_category(self, category_id: str, name: str) -> dict:
        """Редактирование категории."""
        url = self._build_url(f"/api/categories/{category_id}")
        payload = {"name": name}
        response = self.session.put(url, json=payload)
        self._raise_for_status(response)
        return response.json()

    def delete_category(self, category_id: str) -> None:
        """Удаление категории."""
        url = self._build_url(f"/api/categories/{category_id}")
        response = self.session.delete(url)
        self._raise_for_status(response)


class SpendApiClient(BaseHttpClient):
    """HTTP клиент для работы с тратами."""

    def add_spend(self, amount: float, description: str, category_id: str,
                  spend_date: str, currency: str = "RUB") -> dict:
        """Создание траты."""
        url = self._build_url("/api/spends/add")
        payload = {
            "amount": amount,
            "description": description,
            "category": {"id": category_id},
            "spendDate": spend_date,
            "currency": currency,
        }
        response = self.session.post(url, json=payload)
        self._raise_for_status(response)
        return response.json()

    def get_spends(self, limit: Optional[int] = None) -> List[dict]:
        """Получение всех трат."""
        url = self._build_url("/api/spends/all")
        params = {}
        if limit:
            params['limit'] = limit
        response = self.session.get(url, params=params)
        self._raise_for_status(response)
        return response.json()

    def edit_spend(self, spend_id: str, amount: float, description: str,
                   category_id: str, spend_date: str, currency: str = "RUB") -> dict:
        """Редактирование траты."""
        url = self._build_url(f"/api/spends/{spend_id}")
        payload = {
            "amount": amount,
            "description": description,
            "category": {"id": category_id},
            "spendDate": spend_date,
            "currency": currency,
        }
        response = self.session.put(url, json=payload)
        self._raise_for_status(response)
        return response.json()

    def delete_spends(self, spend_ids: List[str]) -> None:
        """Удаление трат."""
        url = self._build_url("/api/spends/remove")
        response = self.session.delete(url, params={"ids": spend_ids})
        self._raise_for_status(response)

    def delete_spend(self, spend_id: str) -> None:
        """Удаление отдельной траты."""
        self.delete_spends([spend_id])

    # Алиасы для обратной совместимости
    def add_spends(self, amount: float, description: str, category: str,
                   currency: str = "RUB", spend_date: str = "2024-10-10") -> dict:
        """Алиас add_spend с упрощённой сигнатурой — принимает имя категории."""
        url = self._build_url("/api/spends/add")
        payload = {
            "amount": amount,
            "description": description,
            "category": {"name": category},   # имя, не id
            "spendDate": spend_date,
            "currency": currency,
        }
        response = self.session.post(url, json=payload)
        self._raise_for_status(response)
        return response.json()

    def remove_spends(self, spend_ids: list) -> None:
        """Алиас delete_spends."""
        self.delete_spends(spend_ids)

