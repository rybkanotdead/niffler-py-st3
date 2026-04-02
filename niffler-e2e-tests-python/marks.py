import pytest


class Pages:
    """Декораторы для пометки тестов страниц."""
    main_page = pytest.mark.usefixtures("main_page")
    # profile_page автоматически вытянет login_user -> auth_page -> browser_setup
    profile_page = pytest.mark.usefixtures("profile_page")


class TestData:
    """Декораторы для параметризации данных тестов."""

    @staticmethod
    def category(category_name: str):
        return pytest.mark.parametrize("category", [category_name], indirect=True)

    @staticmethod
    def spends(spend_data):
        return pytest.mark.parametrize("spends", [spend_data], indirect=True)

    @staticmethod
    def category_db(category_data):
        return pytest.mark.parametrize("category_db", [category_data], indirect=True, ids=lambda param: param.name)
