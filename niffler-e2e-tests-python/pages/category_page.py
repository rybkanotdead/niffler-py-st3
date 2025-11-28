from selene import browser, have, be, by
from selenium.webdriver.common.keys import Keys
import time


class CategoryPage:
    """
    Класс взаимодействия с категориями на странице Профиля.
    """

    def __init__(self):
        self.archived_label = browser.element(by.xpath('//span[text()="Show archived"]'))

        self.confirm_archive_btn = browser.element(
            by.xpath('//div[@role="dialog"]//button[contains(text(), "Archive")]')
        )

        self.archive_icon_xpath = ".//*[local-name()='svg']//*[local-name()='path'][starts-with(@d, 'M5 8H19')]"

        self.pencil_icon_xpath = ".//*[local-name()='svg']//*[local-name()='path'][starts-with(@d, 'M4 16L3')]"

    def find_category_container(self, name: str):
        """Находит строку с категорией по тексту"""
        return browser.element(by.xpath(f'//span[text()="{name}"]/ancestor::div[contains(@class, "MuiChip-root")]'))

    def toggle_show_archived(self):
        """Переключает тумблер 'Show archived' кликом по тексту"""
        self.archived_label.should(be.visible).click()

    def archive_category(self, name: str) -> None:
        """Удаление (архивация) категории"""
        time.sleep(1.0)
        container = self.find_category_container(name).should(be.visible)
        browser.driver.execute_script("arguments[0].scrollIntoView(true);", container.locate())

        container.hover()
        time.sleep(0.2)

        archive_icon = container.element(by.xpath(self.archive_icon_xpath))

        try:
            archive_icon.click()
        except:
            browser.driver.execute_script("arguments[0].click();", archive_icon.locate())

        time.sleep(0.5)
        confirm_btn = self.confirm_archive_btn.should(be.present)
        browser.driver.execute_script("arguments[0].click();", confirm_btn.locate())

    def edit_category_name(self, old_name: str, new_name: str) -> None:
        """Редактирование имени категории"""
        time.sleep(1.0)
        container = self.find_category_container(old_name)
        container.hover()

        pencil_icon = container.element(by.xpath(self.pencil_icon_xpath))
        try:
            pencil_icon.click()
        except:
            browser.driver.execute_script("arguments[0].click();", pencil_icon.locate())

        edit_input = browser.element(f'input[value="{old_name}"]')

        if not edit_input.matching(be.present):
            edit_input = browser.element('form input')

        modifier_key = Keys.COMMAND if 'Mac' in str(browser.driver.capabilities) else Keys.CONTROL

        edit_input.send_keys(modifier_key + 'a')
        edit_input.send_keys(Keys.BACKSPACE)
        edit_input.type(new_name).press_enter()

    def check_category_visible(self, name: str):
        self.find_category_container(name).should(be.visible)

    def check_category_not_visible(self, name: str):
        self.find_category_container(name).should(be.not_.visible)