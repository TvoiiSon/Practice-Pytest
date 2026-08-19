import pytest
import allure
from config import BASE_URL
from playwright.sync_api import Page, expect
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from helpers.data_generator import generate_user

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("Позитивный")
@pytest.mark.smoke
def test_valid_register(page: Page):
    register_page = RegisterPage(page)
    register_page.open()

    user = generate_user()
    register_page.register(**user)
    expect(page).to_have_url(BASE_URL + "/login")

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("Негативный")
@pytest.mark.parametrize("empty_field", ["first_name", "last_name", "email", "password"])
@pytest.mark.regression
def test_empty_fields_register(page: Page, empty_field):
    register_page = RegisterPage(page)
    register_page.open()

    user = generate_user()
    user[empty_field] = ""
    register_page.register(**user)
    validate_locator = getattr(register_page, f"{empty_field}_input")
    assert register_page.is_field_required(validate_locator)

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("Негативный")
@pytest.mark.regression
def test_invalid_password_register(page: Page):
    register_page = RegisterPage(page)
    register_page.open()

    user = generate_user()
    user["password"] = "12345"
    register_page.register(**user)
    assert register_page.is_field_required(register_page.password_input)

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("Негативный")
@pytest.mark.parametrize("invalid_email", ["qwe@qwe", "qwe@qwecom"])
@pytest.mark.regression
def test_invalid_fields_register(page: Page, invalid_email):
    collected = []

    def catch_it(item):
        collected.append(item)
        
    register_page = RegisterPage(page)
    register_page.open()

    user = generate_user()
    user["email"] = invalid_email
    page.on("pageerror", catch_it)
    register_page.register(**user)

    page.wait_for_load_state("networkidle")

    assert collected == []

@allure.severity(allure.severity_level.NORMAL)
@allure.tag("Позитивный")
@pytest.mark.regression
def test_empty_phone_register(page: Page):
    register_page = RegisterPage(page)
    register_page.open()

    user = generate_user()
    user["phone"] = ""
    register_page.register(**user)
    expect(page).to_have_url(BASE_URL + "/login")

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("Негативный")
@pytest.mark.regression
def test_exists_email_register(page: Page):
    register_page = RegisterPage(page)
    register_page.open()

    user = generate_user()
    user["email"] = "test@example.com"
    register_page.register(**user)
    expect(page.get_by_text("Email already registered")).to_be_visible()

@allure.severity(allure.severity_level.NORMAL)
@allure.tag("Позитивный")
@pytest.mark.regression
def test_to_login(page: Page):
    register_page = RegisterPage(page)
    register_page.open()

    register_page.go_to_login()
    expect(page).to_have_url(LoginPage.URL)
