import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.register_page import RegisterPage

@pytest.mark.smoke
def test_valid_login(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("test@example.com", "password123")
    expect(login_page.header.avatar_button).to_be_visible()

@pytest.mark.smoke
def test_invalid_login(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("wrong@example.com", "wpassword")
    expect(page.get_by_text("Incorrect email or password")).to_be_visible()

@pytest.mark.parametrize("empty_field", ["email", "password"])
def test_empty_fields_login(page: Page, empty_field):
    login_page = LoginPage(page)
    login_page.open()

    if empty_field == "email":
        login_page.login("", "password123")
    elif empty_field == "password":
        login_page.login("test@example.com", "")

    validate_locator = getattr(login_page, f"{empty_field}_input")
    assert login_page.is_field_required(validate_locator)

@pytest.mark.regression
def test_go_to_register(page: Page):
    login_page = LoginPage(page)
    login_page.open()

    login_page.go_to_register()
    expect(page).to_have_url(RegisterPage.URL)
