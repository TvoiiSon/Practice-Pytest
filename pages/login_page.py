import allure
from playwright.sync_api import Page
from pages.base_page import BasePage
from config import BASE_URL
from loguru import logger

class LoginPage(BasePage):
    URL = BASE_URL + "/login"

    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = page.get_by_placeholder("user@example.com")
        self.password_input = page.get_by_placeholder("••••••")
        self.login_button = page.get_by_role("button", name="Войти")
        self.register_link = page.get_by_role("link", name="Зарегистрироваться")

    def open(self):
        self.page.goto(self.URL)

    @allure.step("Прохождение авторизации с email: {email}")
    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        logger.info(f"Прохождение авторизации с email: {email}")
        self.login_button.click()

    def get_error_message(self) -> str:
        return self.page.get_by_text("Incorrect email or password").text_content()

    @allure.step("Переход на страницу Регистрации по ссылке внизу формы Авторизации")
    def go_to_register(self):
        logger.info("Переход на страницу Регистрации по ссылке внизу формы Авторизации")
        self.register_link.click()
