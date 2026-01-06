import allure


def assertIsNotNone(variable_, msg: str):
    @allure.step(msg)
    def wrapper(variable):
        assert variable is not None, msg

    wrapper(variable_)


def assertEqual(received_, expected_, msg):
    @allure.step(msg)
    def wrapper(received, expected):
        assert received == expected, f"{msg}\nExpected: {expected}\nReceived: {received}"

    wrapper(received_, expected_)


def assertNotIn(what_, where_, msg):
    @allure.step(msg)
    def wrapper(what, where):
        assert what not in where, msg

    wrapper(what_, where_)