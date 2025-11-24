from selenium.webdriver import Keys
from selene import browser, by


class SpendingPage:

    def __init__(self):
        self.stat_area = browser.element('#stat')
        self.avatar_btn = browser.element('//div[contains(@class, "MuiAvatar-root")]/parent::button')
        self.sign_out_btn = browser.element(by.text('Sign out'))
        self.logout_btn = browser.element(by.text('Log out'))
        self.add_spending_btn = browser.element('a[href="/spending"]')
        self.amount = browser.element('#amount')
        self.currency = browser.element('#currency')
        self.usd_btn = browser.element('[data-value="USD"]')
        self.category = browser.element('#category')
        self.datepicker_input = browser.element('[name="date"]')
        self.datepicker_btn = browser.element('//*[@alt="Calendar"]/parent::button')
        self.datepicker_year_btn = browser.element('//*[@data-testid="ArrowDropDownIcon"]/parent::button')
        self.datepicker_year_choice_btn = browser.element('//button[contains(text(), "2024")]')
        self.datepicker_prev_month_btn = browser.element('button[title="Previous month"]')
        self.datepicker_day_btn = browser.element('//button[contains(text(), "10")]')
        self.description = browser.element('#description')
        self.add_btn = browser.element('#save')
        self.cancel_btn = browser.element('#cancel')

        # --- ИЗМЕНЕНИЕ: Ищем один элемент (тело таблицы), а не список строк ---
        self.table_body = browser.element('tbody')
        # ----------------------------------------------------------------------

        self.table_checkbox = browser.element('//tbody//input[@type="checkbox"]')
        self.table_delete_btn = browser.element('//button[contains(text(), "Delete")]')
        self.delete_button = browser.element('//div[@role="dialog"]//button[contains(text(), "Delete")]')
        self.delete_alert = browser.element('//div[contains(text(), "Spendings succesfully deleted")]')

    def fill_amount(self, amount: int):
        self.amount.type(amount)

    def choose_usd(self):
        self.currency.click()
        self.usd_btn.click()

    def fill_category(self, category: str):
        self.category.type(category)

    def fill_datepicker_input(self, full_date: str):
        self.datepicker_input.send_keys(Keys.COMMAND + 'a')
        self.datepicker_input.send_keys(Keys.BACKSPACE)
        self.datepicker_input.type(full_date)
        self.datepicker_input.press(Keys.TAB)

    def fill_date_picker_btns(self):
        self.datepicker_btn.click()
        self.datepicker_year_btn.click()
        self.datepicker_year_choice_btn.click()
        self.datepicker_prev_month_btn.click()
        self.datepicker_day_btn.click()
        self.datepicker_input.press(Keys.ESCAPE)

    def fill_description(self, description: str):
        self.description.type(description)

    def click_on_add(self):
        self.add_btn.click()

    def click_on_cancel(self):
        self.cancel_btn.click()