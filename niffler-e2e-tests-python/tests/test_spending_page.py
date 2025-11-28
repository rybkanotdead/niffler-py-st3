import random
from selene import have, be


class TestSpending:
    description_1_row = 'test_1'

    def test_add_spendings_datepicker_input(self, spending_page, login_user, cleanup_spendings):
        spending_page.add_spending_btn.click()
        spending_page.fill_amount(amount=random.randint(1, 100))
        spending_page.choose_usd()
        spending_page.fill_category(category='abc')
        spending_page.fill_datepicker_input(full_date='10/10/2024')
        spending_page.fill_description(description=self.description_1_row)
        spending_page.add_btn.click()

        spending_page.table_body.should(have.text(self.description_1_row))

    def test_add_spendings_datepicker_btns(self, spending_page, login_user, cleanup_spendings):
        spending_page.add_spending_btn.click()
        spending_page.fill_amount(amount=random.randint(1, 100))
        spending_page.choose_usd()
        spending_page.fill_category(category='abc')
        spending_page.fill_date_picker_btns()
        spending_page.fill_description(description=self.description_1_row)
        spending_page.add_btn.click()

        spending_page.table_body.should(have.text(self.description_1_row))

    def test_delete_spending(self, spending_page, login_user):
        spending_page.add_spending_btn.click()
        spending_page.fill_amount(100)
        spending_page.choose_usd()
        spending_page.fill_category('delete_test')
        spending_page.fill_description('to delete')
        spending_page.add_btn.click()

        spending_page.table_checkbox.click()
        spending_page.table_delete_btn.click()
        spending_page.delete_button.click()
        spending_page.delete_alert.should(be.visible)

    def test_cancel_adding_spending(self, spending_page, login_user):
        """Отмена создания траты возвращает на главную"""
        spending_page.add_spending_btn.click()
        spending_page.fill_amount(500)
        spending_page.click_on_cancel()
        spending_page.add_spending_btn.should(be.visible)

    def test_add_spending_without_category(self, spending_page, login_user):
        """Негативный: создание без категории"""
        spending_page.add_spending_btn.click()
        spending_page.fill_amount(100)
        spending_page.choose_usd()
        spending_page.fill_description("No category")
        spending_page.add_btn.click()
        spending_page.add_btn.should(be.visible)
        spending_page.click_on_cancel()

    def test_add_spending_zero_amount(self, spending_page, login_user):
        """Негативный: сумма 0"""
        spending_page.add_spending_btn.click()
        spending_page.fill_amount(0)
        spending_page.add_btn.click()
        spending_page.add_btn.should(be.visible)
        spending_page.click_on_cancel()

    def test_add_spending_max_amount(self, spending_page, login_user, cleanup_spendings):
        """Граничные значения: большая сумма"""
        spending_page.add_spending_btn.click()
        spending_page.fill_amount(999999)
        spending_page.choose_usd()
        spending_page.fill_category("Rich")
        spending_page.add_btn.click()

        # ПРОВЕРКА ОБНОВЛЕНА
        spending_page.table_body.should(have.text("Rich"))

    def test_check_currency_selection(self, spending_page, login_user):
        """UI: Проверка выбора валюты"""
        spending_page.add_spending_btn.click()
        spending_page.currency.click()
        spending_page.usd_btn.should(be.visible)
        spending_page.usd_btn.click()
        spending_page.click_on_cancel()

    def test_logout_from_spending_page(self, spending_page, login_user, auth_page):
        """Сценарий выхода из системы"""
        spending_page.avatar_btn.click()
        spending_page.sign_out_btn.click()
        spending_page.logout_btn.click()
        auth_page.login_btn.should(be.visible)