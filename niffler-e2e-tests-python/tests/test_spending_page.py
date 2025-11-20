import random

from selene import have, be
from pages.auth_reg_page import AuthRegistrationPage
from pages.spendings_page import SpendingPage
from faker import Faker

auth_page = AuthRegistrationPage()
spending_page = SpendingPage()
faker = Faker()


class TestSpending:

    description_1_row = 'test_1'
    description_2_row = 'test_2'

    def test_add_spendings_datepicker_input(self):
        spending_page.open_spending_page()
        spending_page.add_spending_btn.click()
        spending_page.fill_amount(amount=random.randint(1, 100))
        spending_page.currency.click()
        spending_page.usd_btn.click()
        spending_page.fill_category(category='abc')
        spending_page.fill_datepicker_input(full_date='10/10/2024')
        spending_page.fill_description(description=self.description_1_row)
        spending_page.add_btn.click()
        spending_page.table_description_first_row.should(have.text(self.description_1_row))
        spending_page.table_checkbox.click()
        spending_page.table_delete_btn.click()
        spending_page.delete_button.click()


    def test_add_spendings_datepicker_btns(self):
        spending_page.open_spending_page()
        spending_page.add_spending_btn.click()
        spending_page.fill_amount(amount=random.randint(1, 100))
        spending_page.currency.click()
        spending_page.usd_btn.click()
        spending_page.fill_category(category='abc')
        spending_page.fill_date_picker_btns()
        spending_page.fill_description(description=self.description_1_row)
        spending_page.add_btn.click()
        spending_page.table_description_first_row.should(have.text(self.description_1_row))
        spending_page.table_checkbox.click()
        spending_page.table_delete_btn.click()
        spending_page.delete_button.click()


    def test_delete_spending(self):
        spending_page.add_spending()
        spending_page.table_checkbox.click()
        spending_page.table_delete_btn.click()
        spending_page.delete_button.click()
        spending_page.delete_alert.should(be.visible)
