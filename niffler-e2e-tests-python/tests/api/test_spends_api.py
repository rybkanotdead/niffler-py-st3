import allure
import pytest
from modals.enums import Category, Currency
from modals.spend import SpendAdd, SpendEdit
from utils.api_assertions import assertEqual, assertNotIn
from utils.datetime_helper import get_past_date_iso


@allure.feature('Таблица трат')
@allure.story('API')
class TestSpendsApi:

    @pytest.fixture
    def created_spend(self, spends_client):
        """Фикстура: создает трату для тестов удаления и редактирования"""
        with allure.step('Setup: Создать предварительную трату'):
            spend_data = SpendAdd(
                amount=101.1,
                description="test_description",
                category=Category.TEST_CATEGORY,
                spendDate=get_past_date_iso(),
                currency=Currency.RUB
            )
            return spends_client.add_spends(spend_data)

    @allure.title('Создание траты через API')
    def test_add_spend_api(self, spends_client, envs, clean_categories, clean_spendings_setup):
        # Arrange
        spend_data = SpendAdd(
            amount=101.1,
            description="test_description",
            category=Category.TEST_CATEGORY,
            spendDate=get_past_date_iso(),
            currency=Currency.RUB
        )

        # Act
        with allure.step('Отправить запрос на создание траты'):
            new_spend = spends_client.add_spends(spend_data)

        # Assert
        with allure.step('Проверить соответствие данных в ответе'):
            assertEqual(new_spend.amount, spend_data.amount, "Сумма совпадает")
            assertEqual(new_spend.description, spend_data.description, "Описание совпадает")
            # Обратите внимание: SpendAdd принимает category, но ответ возвращает объект Category
            assertEqual(new_spend.category.name, spend_data.category, "Категория совпадает")
            assertEqual(new_spend.currency, spend_data.currency, "Валюта совпадает")

    @allure.title('Удаление траты через API')
    def test_delete_spend_api(self, spends_client, created_spend):
        # Act
        with allure.step(f'Удалить трату с ID {created_spend.id}'):
            spends_client.remove_spends([created_spend.id])  # Обычно remove принимает список ID

        # Assert
        with allure.step('Проверить отсутствие траты в списке'):
            all_spends = spends_client.get_spends()
            # Собираем ID всех трат в список для проверки
            all_ids = [s.id for s in all_spends]
            assertNotIn(created_spend.id, all_ids, "Удаленная трата не найдена в списке")

    @allure.title('Редактирование траты через API')
    def test_edit_spend_api(self, spends_client, created_spend):
        # Arrange
        new_amount = 555.0
        new_desc = "Измененное описание"

        edit_data = SpendEdit(
            id=created_spend.id,
            spendDate=created_spend.spendDate,  # Оставляем дату старой
            amount=new_amount,
            category=created_spend.category,  # Оставляем категорию старой (объект)
            description=new_desc,
            currency=Currency.USD
        )

        # Act
        with allure.step('Редактировать трату'):
            edited_spend = spends_client.edit_spend(edit_data)

        # Assert
        assertEqual(edited_spend.amount, new_amount, "Сумма обновилась")
        assertEqual(edited_spend.description, new_desc, "Описание обновилось")
        assertEqual(edited_spend.currency, Currency.USD, "Валюта обновилась")

    @allure.title('Создание траты со всеми поддерживаемыми валютами')
    @pytest.mark.parametrize("currency, amount, desc", [
        (Currency.RUB, 1000.50, "Трата в рублях"),
        (Currency.USD, 100.75, "Трата в долларах"),
        (Currency.EUR, 90.25, "Трата в евро"),
        (Currency.KZT, 50000.0, "Трата в тенге")
    ])
    def test_add_spend_currencies_api(self, spends_client, currency, amount, desc):
        # Arrange
        spend_data = SpendAdd(
            amount=amount,
            description=desc,
            category=Category.TEST_CATEGORY,
            spendDate=get_past_date_iso(),
            currency=currency
        )

        # Act
        with allure.step(f'Создать трату: {amount} {currency}'):
            new_spend = spends_client.add_spends(spend_data)

        # Assert
        assertEqual(new_spend.currency, currency, "Валюта сохранена корректно")
        assertEqual(new_spend.amount, amount, "Сумма сохранена корректно")