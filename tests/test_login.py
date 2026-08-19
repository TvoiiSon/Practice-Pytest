import pytest
import allure
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.header_component import HeaderComponent
from models.user import User, UserLoginAPIResponse

@allure.tag("Позитивный")
@pytest.mark.smoke
def test_valid_login(page: Page):
    login_page = LoginPage(page)
    login_page.open()

    login_page.login("test@example.com", "password123")

    expect(login_page.header.avatar_button).to_be_visible()
    assert page.evaluate("localStorage.getItem('token')")

@allure.tag("Позитивный")
@pytest.mark.api
def test_valid_answer_me_api(authenticated_page: Page):
    token = authenticated_page.evaluate("localStorage.getItem('token')")

    request = authenticated_page.request.get("https://archiscope.ru/api/users/me", headers={'Authorization': f'Bearer {token}'}).json()
    assert User(**request)

@allure.tag("Позитивный")
@pytest.mark.api
def test_valid_answer_login_api(page: Page):
    request = page.request.post(url="https://archiscope.ru/api/auth/login", multipart={"username": "test@example.com", "password": "password123"})
    assert request.status == 200
    request = request.json()
    assert UserLoginAPIResponse(**request)

@allure.tag("Негативный")
@pytest.mark.regression
def test_invalid_login(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("wrong@example.com", "wpassword")
    expect(page.get_by_text("Incorrect email or password")).to_be_visible()

@allure.tag("Негативный")
@pytest.mark.parametrize("empty_field", ["email", "password"])
@pytest.mark.regression
def test_empty_fields_login(page: Page, empty_field):
    login_page = LoginPage(page)
    login_page.open()

    if empty_field == "email":
        login_page.login("", "password123")
    elif empty_field == "password":
        login_page.login("test@example.com", "")

    validate_locator = getattr(login_page, f"{empty_field}_input")
    assert login_page.is_field_required(validate_locator)

@allure.tag("Позитивный")
@pytest.mark.regression
def test_logout(authenticated_page: Page):
    header_component = HeaderComponent(authenticated_page)
    header_component.logout()
    assert authenticated_page.evaluate("localStorage.getItem('token')") is None

@allure.tag("Позитивный")
@pytest.mark.regression
def test_go_to_register(page: Page):
    login_page = LoginPage(page)
    login_page.open()

    login_page.go_to_register()
    expect(page).to_have_url(RegisterPage.URL)
