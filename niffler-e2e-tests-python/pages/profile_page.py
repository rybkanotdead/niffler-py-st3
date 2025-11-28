from selene import browser, have


class ProfilePage:
    """
    Класс взаимодействия с UI страницей Профиля пользователя
    """

    def __init__(self):
        self.input_category = browser.element('#category')
        self.alert = browser.element('div[role="alert"] div:nth-child(2)')
        self.error_alert = browser.element('.add-category__input-container button')
        self.name = browser.element('#name')
        self.submit_button = browser.element('button[type=submit]')

        self.profile_title = browser.element('h2')

    def add_category(self, category: str):
        """
        Метод добавления категории
        :param category: наименование категории
        """
        self.input_category.type(category).press_enter()

    def successful_adding(self, category: str):
        """
        Метод проверки сигнального сообщения об успешном добавлении категории
        :param category: наименование категории
        """
        self.alert.should(have.text(f"You've added new category: {category}"))

    def check_error_message(self, message: str):
        """
        Метод проверки alert сообщения
        :param message: текст ошибки
        """
        self.alert.should(have.text(message))

    def adding_empty_name_category(self):
        """
        Метод добавления категории без наименования
        """
        self.input_category.type('  ').press_enter()

    def add_user_name(self, name: str):
        """
        Метод добавления имени в профиле пользователя
        :param name: имя пользователя
        """
        self.name.clear()
        self.name.type(name)
        self.submit_button.click()

    def check_successful_adding_name(self):
        """
        Метод проверки сигнального сообщения об успешном добавлении имени пользователя
        """
        self.alert.should(have.text("Profile successfully updated"))

    def check_profile_title(self, title: str):
        """
        Метод проверки заголовка профайла пользователя
        :param title: Заголовок профайла
        """
        self.profile_title.should(have.text(title))