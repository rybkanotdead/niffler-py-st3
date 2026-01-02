import allure
from selene import browser, have, be


class SpendingPage:
    def __init__(self):
        self.stat_area = browser.element('#spendings')
        self.avatar_btn = browser.element('.header__avatar')
        self.sign_out_btn = browser.element('button.dropdown-item:last-child')  # Кнопка выхода в меню

        # Элементы таблицы и модалок
        self.add_spending_btn = browser.element('a[href="/spending"]')
        self.table_body = browser.element('.spendings-table tbody')
        self.table_checkbox = browser.element('.spendings-table tbody input[type="checkbox"]')
        self.table_delete_btn = browser.element('.spendings__bulk-actions button')

        self.delete_button = browser.element('.modal-footer .btn-danger')  # Кнопка Delete в модалке
        self.delete_alert = browser.element('.Toastify__toast--success')  # Тост успеха

    def logout(self):
        """Метод выхода из системы"""
        with allure.step('Выполнить выход (Logout)'):
            self.avatar_btn.click()
            self.sign_out_btn.click()

            # Если есть подтверждение выхода в модальном окне, добавьте клик сюда.
            # Если выхода сразу происходит - этот метод готов.
            # browser.element('.modal-footer .btn-primary').click()