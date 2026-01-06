import requests
from modals.config import Envs
from modals.spend import Spend, SpendAdd, SpendEdit
from modals.category import CategorySQL
from utils.sessions import BaseSession


class SpendsHttpClient:
    """Http-клиент"""

    session: requests.Session
    base_url: str

    def __init__(self, envs: Envs, token: str):
        self.session = BaseSession(base_url=envs.api_url)
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

    def get_categories(self) -> list[CategorySQL]:
        response = self.session.get("/api/categories/all")
        return [CategorySQL.model_validate(item) for item in response.json()]

    def add_category(self, name: str) -> CategorySQL:
        response = self.session.post("/api/categories/add", json={
            "name": name
        })
        return CategorySQL.model_validate(response.json())

    def edit_category(self, category: CategorySQL) -> CategorySQL:
        category_data = CategorySQL.model_validate(category)
        response = self.session.patch("/api/categories/update", json=category_data.model_dump())
        return CategorySQL.model_validate(response.json())

    def get_spends(self) -> list[Spend]:
        response = self.session.get("/api/spends/all")
        return [Spend.model_validate(item) for item in response.json()]

    def add_spends(self, spend: SpendAdd) -> Spend:
        spend_data = SpendAdd.model_validate(spend)
        response = self.session.post("/api/spends/add", json=spend_data.model_dump())
        return Spend.model_validate(response.json())

    def edit_spend(self, edit_spend: SpendEdit) -> Spend:
        response = self.session.patch("/api/spends/edit", data=edit_spend.model_dump_json())
        print(response.json())
        return Spend.model_validate(response.json())

    def remove_spends(self, ids: list[str]):
        """Удааление трат"""
        response = self.session.delete("/api/spends/remove", params={"ids": ids})
        return response