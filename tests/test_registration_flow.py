import pytest
from config import BASE_URL
from playwright.sync_api import Page, expect
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from helpers.data_generator import generate_user

@pytest.mark.regression
def test_flow_register_login(page: Page):
    login_page = LoginPage(page)
    register_page = RegisterPage(page)

    register_page.open()

    user = generate_user()
    register_page.register(**user)

    expect(page).to_have_url(BASE_URL + "/login")

    login_page.login(user["email"], user["password"])

    expect(login_page.header.avatar_button).to_be_visible()
