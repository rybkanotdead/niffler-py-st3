import json
import requests
import allure
from urllib.parse import urljoin

from modals.spend import Spend, SpendAdd


class SpendsHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        })

    def add_spends(self, spend: SpendAdd) -> Spend:
        endpoint = "/api/spends/add"
        url = urljoin(self.base_url, endpoint)
        body = spend.model_dump()

        with allure.step(f"API: POST {endpoint}"):
            allure.attach(
                json.dumps(body, indent=2, ensure_ascii=False),
                name="Request Body",
                attachment_type=allure.attachment_type.JSON
            )

            response = self.session.post(url, json=body)

            self._attach_response(response)

            self.raise_for_status(response)
            return Spend.model_validate(response.json())

    def get_spends(self) -> list[Spend]:
        endpoint = '/api/spends/all'
        url = urljoin(self.base_url, endpoint)

        with allure.step(f"API: GET {endpoint}"):
            response = self.session.get(url)

            # Прикладываем Response Body
            self._attach_response(response)

            self.raise_for_status(response)
            return [Spend.model_validate(item) for item in response.json()]

    def remove_spends(self, ids: list[str]) -> None:
        endpoint = "/api/spends/remove"
        url = urljoin(self.base_url, endpoint)
        params = {"ids": ids}

        with allure.step(f"API: DELETE {endpoint}"):
            allure.attach(
                json.dumps(params, indent=2),
                name="Query Params",
                attachment_type=allure.attachment_type.JSON
            )

            response = self.session.delete(url, params=params)

            self._attach_response(response)

            self.raise_for_status(response)

    @staticmethod
    def raise_for_status(response: requests.Response):
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == 400:
                e.add_note(response.text)
                raise

    def _attach_response(self, response: requests.Response):
        """Хелпер для прикрепления ответа к аллюру"""
        try:
            content = json.dumps(response.json(), indent=2, ensure_ascii=False)
            allure.attach(
                content,
                name=f"Response {response.status_code}",
                attachment_type=allure.attachment_type.JSON
            )
        except Exception:
            if response.text:
                allure.attach(
                    response.text,
                    name=f"Response {response.status_code}",
                    attachment_type=allure.attachment_type.TEXT
                )
            else:
                allure.attach(
                    f"Status code: {response.status_code}",
                    name="Response Status",
                    attachment_type=allure.attachment_type.TEXT
                )