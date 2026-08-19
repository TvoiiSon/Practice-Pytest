import allure
from playwright.sync_api import Page
from pages.base_page import BasePage
from config import BASE_URL
from loguru import logger

class ProfilePage(BasePage):
    URL = BASE_URL + "/profile"

    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input = page.locator('input[name="first_name"]')
        self.last_name_input = page.locator('input[name="last_name"]')
        self.email_input = page.locator('input[name="email"]')
        self.phone_input = page.locator('input[name="phone"]')
        self.password_input = page.locator('input[name="password"]')
        self.image_input = page.locator('input[type="file"]')
        self.save_button = page.get_by_role("button", name="Сохранить")

    def open(self):
        self.page.goto(self.URL)

    @allure.step("Обновления профиля с новым Именем: {first_name}, Фамилией: {last_name}, Email: {email}")
    def update_profile(self, first_name: str, last_name: str, email: str, phone: str = "", password: str = "", image_path: str = ""):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.email_input.fill(email)
        if phone:
            self.phone_input.fill(phone)
        if password:
            self.password_input.fill(password)
        if image_path:
            self.image_input.set_input_files(image_path)
        logger.info(f"Обновления профиля с новым Именем: {first_name}, Фамилией: {last_name}, Email: {email}")
        self.save_button.click()
