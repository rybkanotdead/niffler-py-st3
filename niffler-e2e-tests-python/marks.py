import pytest


class Pages:
    """Декораторы для пометки тестов страниц"""
    main_page = pytest.mark.usefixtures("main_page")
    main_page_late = pytest.mark.usefixtures("main_page_late")
    profile_page = pytest.mark.usefixtures("auth_page", "profile_page")
    profile_page_db = pytest.mark.usefixtures("profile_page", "db")
    login_page = pytest.mark.usefixtures("login_page")

    @staticmethod
    def delete_spend(name_category):
        return pytest.mark.parametrize("delete_spend_fx", [name_category], indirect=True)


class TestData:
    """Декораторы для параметризации данных тестов"""

    @staticmethod
    def category(category_name: str):
        return pytest.mark.parametrize("category", [category_name], indirect=True)

    @staticmethod
    def spends(spend_data):
        return pytest.mark.parametrize("spends", [spend_data], indirect=True)

    @staticmethod
    def category_db(category_data):
        return pytest.mark.parametrize("category_db", [category_data], indirect=True, ids=lambda param: param.name)
