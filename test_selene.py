import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


def test_search_for_selene(browser):
    page_instance = browser.new_page()
    page_instance.goto("https://www.google.com")

    search_field = page_instance.locator('textarea[name="q"]')
    search_query = "yashaka//selene"
    search_field.fill(search_query)
    search_field.press('Enter')
    page_instance.wait_for_load_state()

    multiple_options_selector = '[id="res"] div span a[jsname="UWckNb"]:first-child'
    page_instance.query_selector_all(multiple_options_selector)[0].click()
    page_instance.wait_for_load_state()

    page_content = page_instance.inner_text("html").lower()

    word_for_search = "selene"
    occurrences_count = page_content.count(word_for_search.lower())

    print(f'\nThe word "{word_for_search}" occurs {occurrences_count} times on the page {page_instance.url}.')

    page_instance.close()
