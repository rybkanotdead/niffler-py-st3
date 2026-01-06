from dataclasses import dataclass


@dataclass
class Category:
    TEST_CATEGORY = "test_category"
    TEST_CATEGORY_2 = "another_category"
    TEST_CATEGORY_BD = "test_category_bd"


@dataclass
class Currency:
    RUB = "RUB"
    KZT = "KZT"
    EUR = "EUR"
    USD = "USD"