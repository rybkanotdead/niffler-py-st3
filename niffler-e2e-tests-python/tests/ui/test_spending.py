import pytest
from selene import browser, have, command
from marks import Pages, TestData
from modals.spend import SpendAdd

pytestmark = [pytest.mark.allure_label("Spendings", label_type="epic")]


@Pages.main_page
def test_spending_title_exists():
    browser.element('.main-content').should(have.text('History of spendings'))


TEST_CATEGORY = "school"


@pytest.fixture()
def main_page_late(category, spends, envs):
    browser.open(envs.frontend_url)


@pytest.mark.usefixtures("main_page_late")
@TestData.category(TEST_CATEGORY)
@TestData.spends(
    SpendAdd(
        amount=108.51,
        description="QA.GURU Python Advanced 1",
        category=TEST_CATEGORY,
        spendDate="2024-08-08T18:39:27.955Z",
        currency="RUB"
    )
)
def test_spending_should_be_deleted_after_table_action(category, spends):
    browser.element('.spendings-table tbody').should(have.text("QA.GURU Python Advanced 1"))
    browser.element('.spendings-table tbody input[type=checkbox]').perform(command.js.scroll_into_view).click()
    browser.element('.spendings__bulk-actions button').click()

    browser.all(".spendings-table tbody tr").should(have.size(0))
    browser.element('.spendings__content').should(have.text("No spendings provided yet!"))