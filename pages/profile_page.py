from playwright.sync_api import Page
from pages.base_page import BasePage
from config import BASE_URL

class ProfilePage(BasePage):
    URL = BASE_URL + "/profile"

    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input = page.locator('input[name="first_name"]')
        self.last_name_input = page.locator('input[name="last_name"]')
        self.email_input = page.locator('input[name="email"]')
        self.phone_input = page.locator('input[name="phone"]')
        self.password_input = page.locator('input[name="password"]')
        self.save_button = page.get_by_role("button", name="Сохранить")

    def open(self):
        self.page.goto(self.URL)

    def update_phone(self, phone: str):
        self.phone_input.fill(phone)
        self.save_button.click()

    def is_update_success_visible(self) -> bool:
        return self.page.get_by_text("Профиль обновлён").is_visible()
