import allure
from playwright.sync_api import Page
from pages.header_component import HeaderComponent
from loguru import logger

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.header = HeaderComponent(page)

    @allure.step("Проверка поля на обязательное")
    def is_field_required(self, locator) -> bool:
        logger.info("Проверка поля на обязательное")
        return locator.evaluate("el => !el.checkValidity()")
    