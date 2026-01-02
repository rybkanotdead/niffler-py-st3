import random
import allure
from selene import have, be


@allure.feature("Управление Тратами")
class TestSpending:
    description_1_row = 'test_1'

    @allure.story("Создание трат")
    @allure.title("Создание траты с ручным вводом даты (Datepicker Input)")
    def test_add_spendings_datepicker_input(self, spending_page, login_user, cleanup_spendings):
        amount = random.randint(1, 100)
        category = 'abc'
        date = '10/10/2024'

        with allure.step(f"Заполнить форму траты: Сумма={amount}, Категория={category}, Дата={date}"):
            spending_page.add_spending_btn.click()
            spending_page.fill_amount(amount=amount)
            spending_page.choose_usd()
            spending_page.fill_category(category=category)
            spending_page.fill_datepicker_input(full_date=date)
            spending_page.fill_description(description=self.description_1_row)
            spending_page.add_btn.click()

        with allure.step(f"ОР: Трата с описанием '{self.description_1_row}' появилась в таблице"):
            spending_page.table_body.should(have.text(self.description_1_row))

    @allure.story("Создание трат")
    @allure.title("Создание траты с выбором даты через виджет (Datepicker Buttons)")
    def test_add_spendings_datepicker_btns(self, spending_page, login_user, cleanup_spendings):
        amount = random.randint(1, 100)

        with allure.step("Заполнить форму траты, выбирая дату через календарь"):
            spending_page.add_spending_btn.click()
            spending_page.fill_amount(amount=amount)
            spending_page.choose_usd()
            spending_page.fill_category(category='abc')
            spending_page.fill_date_picker_btns()
            spending_page.fill_description(description=self.description_1_row)
            spending_page.add_btn.click()

        with allure.step(f"ОР: Трата с описанием '{self.description_1_row}' появилась в таблице"):
            spending_page.table_body.should(have.text(self.description_1_row))

    @allure.story("Удаление трат")
    @allure.title("Удаление существующей траты")
    def test_delete_spending(self, spending_page, login_user):
        # Pre-condition
        with allure.step("Pre-condition: Создать трату для удаления"):
            spending_page.add_spending_btn.click()
            spending_page.fill_amount(100)
            spending_page.choose_usd()
            spending_page.fill_category('delete_test')
            spending_page.fill_description('to delete')
            spending_page.add_btn.click()

        # Action
        with allure.step("Выбрать трату в таблице и нажать удалить"):
            spending_page.table_checkbox.click()
            spending_page.table_delete_btn.click()

        with allure.step("Подтвердить удаление в модальном окне"):
            spending_page.delete_button.click()

        # Assert
        with allure.step("ОР: Отображается алерт об успешном удалении"):
            spending_page.delete_alert.should(be.visible)

    @allure.story("Отмена действий")
    @allure.title("Отмена создания траты")
    def test_cancel_adding_spending(self, spending_page, login_user):
        with allure.step("Открыть форму и ввести данные"):
            spending_page.add_spending_btn.click()
            spending_page.fill_amount(500)

        with allure.step("Нажать кнопку 'Cancel'"):
            spending_page.click_on_cancel()

        with allure.step("ОР: Модальное окно закрылось, видна кнопка добавления"):
            spending_page.add_spending_btn.should(be.visible)

    @allure.story("Валидация формы")
    @allure.title("Негативный: Попытка создания траты без категории")
    def test_add_spending_without_category(self, spending_page, login_user):
        with allure.step("Заполнить форму без указания категории и нажать 'Add'"):
            spending_page.add_spending_btn.click()
            spending_page.fill_amount(100)
            spending_page.choose_usd()
            spending_page.fill_description("No category")
            spending_page.add_btn.click()

        with allure.step("ОР: Трата не создалась, кнопка 'Add' все еще видна (форма не закрылась)"):
            spending_page.add_btn.should(be.visible)

        # Post-condition
        spending_page.click_on_cancel()

    @allure.story("Валидация формы")
    @allure.title("Негативный: Попытка создания траты с суммой 0")
    def test_add_spending_zero_amount(self, spending_page, login_user):
        with allure.step("Ввести сумму 0 и нажать 'Add'"):
            spending_page.add_spending_btn.click()
            spending_page.fill_amount(0)
            spending_page.add_btn.click()

        with allure.step("ОР: Трата не создалась, форма осталась открытой"):
            spending_page.add_btn.should(be.visible)

        # Post-condition
        spending_page.click_on_cancel()

    @allure.story("Граничные значения")
    @allure.title("Создание траты с максимальной суммой")
    def test_add_spending_max_amount(self, spending_page, login_user, cleanup_spendings):
        large_amount = 999999
        category = "Rich"

        with allure.step(f"Создать трату с суммой {large_amount}"):
            spending_page.add_spending_btn.click()
            spending_page.fill_amount(large_amount)
            spending_page.choose_usd()
            spending_page.fill_category(category)
            spending_page.add_btn.click()

        with allure.step(f"ОР: Трата с категорией '{category}' появилась в таблице"):
            spending_page.table_body.should(have.text(category))

    @allure.story("Элементы UI")
    @allure.title("Проверка выпадающего списка выбора валюты")
    def test_check_currency_selection(self, spending_page, login_user):
        with allure.step("Открыть форму создания траты"):
            spending_page.add_spending_btn.click()

        with allure.step("Открыть список валют и выбрать USD"):
            spending_page.currency.click()
            spending_page.usd_btn.should(be.visible)
            spending_page.usd_btn.click()

        with allure.step("Закрыть форму"):
            spending_page.click_on_cancel()

    @allure.story("Навигация и Авторизация")
    @allure.title("Выход из системы (Logout) со страницы трат")
    def test_logout_from_spending_page(self, spending_page, login_user, auth_page):
        with allure.step("Нажать на аватар -> Sign Out -> Logout"):
            spending_page.avatar_btn.click()
            spending_page.sign_out_btn.click()
            spending_page.logout_btn.click()

        with allure.step("ОР: Пользователь перенаправлен на страницу входа"):
            auth_page.login_btn.should(be.visible)