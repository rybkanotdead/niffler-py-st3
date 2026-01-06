import allure
from playwright.sync_api import Page
from pages.base_page import BasePage
from faker import Faker


class SpendingPage(BasePage):
    def __init__(self, page: Page, front_url):
        super().__init__(page)
        self.faker = Faker()
        self.front_url = front_url

        self.spendings_table = page.locator("[id='spendings']")
        self.checkbox_table = page.locator("[type='checkbox']")
        self.category_spending_sum = page.locator("[style*='align-items: center']")

        self.edit_spending_button = page.locator("[aria-label='Edit spending']")
        self.delete_spending_button = page.locator("[id='delete']")

        self.search_input = page.locator("[placeholder='Search']")

        self.new_spending = page.locator("[href='/spending']")
        self.amount_input = page.locator("[id='amount']")
        self.category_input = page.locator("[id='category']")
        self.description_input = page.locator("[id='description']")
        self.add_button = page.locator("[id='save']")

        self.profile_menu = page.locator("[data-testid='PersonIcon']")

    def navigate_to_spending_page(self):
        with allure.step('Перейти на страницу трат'):
            self.go_to(self.front_url)
            self.wait_for_load()

    def click_new_spending(self):
        with allure.step('Перейти к занесению новой траты'):
            self.new_spending.click()
            self.wait_for_load()

    def fill_amount(self, amount: int):
        with allure.step('Заполнить сумму'):
            self.amount_input.fill(f'{amount}')

    def fill_category(self, category: str):
        with allure.step('Заполнить категорию'):
            self.category_input.fill(category)

    def fill_description(self, description: str):
        with allure.step('Заполнить описание'):
            self.description_input.fill(description)

    def click_add(self):
        with allure.step('Нажать "Добавить"'):
            self.add_button.click()
            self.wait_for_load()

    def add_new_spending(self, amount, category, description):
        with allure.step('Добавить новую трату'):
            self.fill_amount(amount)
            self.fill_category(category)
            self.fill_description(description)
            self.click_add()
            self.page.get_by_text("New spending is successfully created").wait_for(state='visible')

    def edit_spending(self, amount, category, description):
        with allure.step('Отредактировать трату'):
            self.fill_amount(amount)
            self.fill_category(category)
            self.fill_description(description)
            self.click_add()
            self.page.get_by_text("Spending is edited successfully").wait_for(state='visible')

    def delete_spending(self):
        with allure.step('Удалить трату'):
            self.checkbox_table.last.click()
            self.delete_spending_button.click()
            self.page.get_by_text('Delete').last.click()

    def delete_all_spendings(self):
        with allure.step('Удалить все траты'):
            self.checkbox_table.first.click()
            self.delete_spending_button.click()
            self.page.get_by_text('Delete').last.click()

    def search_spending(self, input_word: str):
        with allure.step(f'Найти трату: {input_word}'):
            self.search_input.fill(input_word)
            self.page.keyboard.press("Enter")

    def logout(self):
        with allure.step('Выйти из системы'):
            self.profile_menu.click()
            self.page.get_by_text("Sign out").click()
            self.page.get_by_text("Log out").click()