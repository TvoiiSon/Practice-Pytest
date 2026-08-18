import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage

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