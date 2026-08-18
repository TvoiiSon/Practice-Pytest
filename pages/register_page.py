from playwright.sync_api import Page
from pages.base_page import BasePage
from config import BASE_URL

class RegisterPage(BasePage):
    URL = BASE_URL + "/register"

    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input = page.locator('input[name="first_name"]')
        self.last_name_input = page.locator('input[name="last_name"]')
        self.email_input = page.locator('input[name="email"]')
        self.password_input = page.locator('input[name="password"]')
        self.phone_input = page.locator('input[name="phone"]')
        self.register_button = page.get_by_role("button", name="Зарегистрироваться")

    def open(self):
        self.page.goto(self.URL)

    def register(self, first_name: str, last_name: str, email: str,
                 password: str, phone: str = ""):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.email_input.fill(email)
        self.password_input.fill(password)
        if phone:
            self.phone_input.fill(phone)
        self.register_button.click()

    def is_value_invalid(self, locator) -> bool:
        return locator.evaluate("el => !el.checkValidity()")
