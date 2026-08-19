import pytest
import allure
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.header_component import HeaderComponent
from models.user import User, UserLoginAPIResponse
from loguru import logger

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("Позитивный")
@pytest.mark.smoke
@pytest.mark.ui
def test_valid_login(page: Page):
    login_page = LoginPage(page)
    login_page.open()

    login_page.login("test@example.com", "password123")

    expect(login_page.header.avatar_button, message="Аватар не появился в шапке — авторизация не прошла успешно").to_be_visible()
    assert page.evaluate("localStorage.getItem('token')"), "Токен не сохранился в localStorage после успешной авторизации"

@allure.severity(allure.severity_level.NORMAL)
@allure.tag("Позитивный")
@pytest.mark.api
def test_valid_answer_me_api(authenticated_page: Page):
    with allure.step("Запрос /api/users/me с Bearer-токеном — проверка схемы через Pydantic-модель User"):
        token = authenticated_page.evaluate("localStorage.getItem('token')")

        logger.info("Запрос /api/users/me с Bearer-токеном — проверка схемы через Pydantic-модель User")
        request = authenticated_page.request.get("https://archiscope.ru/api/users/me", headers={'Authorization': f'Bearer {token}'}).json()
        assert User(**request)

@allure.severity(allure.severity_level.NORMAL)
@allure.tag("Позитивный")
@pytest.mark.api
def test_valid_answer_login_api(page: Page):
    with allure.step("Запрос POST /api/auth/login напрямую, username: test@example.com — проверка статуса и схемы ответа"):
        logger.info("Запрос POST /api/auth/login напрямую, username: test@example.com — проверка статуса и схемы ответа")
        request = page.request.post(url="https://archiscope.ru/api/auth/login", multipart={"username": "test@example.com", "password": "password123"})
        assert request.status == 200, f"Ожидали статус 200, получили {request.status}"
        request = request.json()
        assert UserLoginAPIResponse(**request)

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("Негативный")
@pytest.mark.regression
@pytest.mark.ui
def test_invalid_login(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("wrong@example.com", "wpassword")
    expect(page.get_by_text("Incorrect email or password"), message="Сообщение об ошибке неверных учётных данных не появилось").to_be_visible()

@allure.severity(allure.severity_level.NORMAL)
@allure.tag("Негативный")
@pytest.mark.parametrize("empty_field", ["email", "password"])
@pytest.mark.regression
@pytest.mark.ui
def test_empty_fields_login(page: Page, empty_field):
    login_page = LoginPage(page)
    login_page.open()

    if empty_field == "email":
        login_page.login("", "password123")
    elif empty_field == "password":
        login_page.login("test@example.com", "")

    validate_locator = getattr(login_page, f"{empty_field}_input")
    assert login_page.is_field_required(validate_locator), f"Поле {empty_field} является обязательным для заполнения"

@allure.severity(allure.severity_level.NORMAL)
@allure.tag("Позитивный")
@pytest.mark.regression
@pytest.mark.ui
def test_logout(authenticated_page: Page):
    header_component = HeaderComponent(authenticated_page)
    header_component.logout()
    assert authenticated_page.evaluate("localStorage.getItem('token')") is None, "Токен остался в localStorage после выхода из аккаунта"

@allure.severity(allure.severity_level.NORMAL)
@allure.tag("Позитивный")
@pytest.mark.regression
@pytest.mark.ui
def test_go_to_register(page: Page):
    login_page = LoginPage(page)
    login_page.open()

    login_page.go_to_register()
    expect(page, message="Переход по ссылке на страницу регистрации не произошёл").to_have_url(RegisterPage.URL)
