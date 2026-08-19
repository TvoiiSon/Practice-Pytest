from playwright.sync_api import Page
from pages.base_page import BasePage
from loguru import logger

class ArticlePage(BasePage):
    def __init__(self, page: Page, title: str = None):
        super().__init__(page)
        self.title = title
        self.comment_input = page.get_by_role("textbox", name="Оставьте комментарий")
        self.submit_comment_button = page.get_by_role("button", name="Отправить")
        self.heading = page.get_by_role("heading", name=title)

    def add_comment(self, text: str):
        self.comment_input.fill(text)
        logger.info(f"Создание комментария: {text} для новости с Названием: {self.title}")
        self.submit_comment_button.click()

    def is_field_required(self, locator) -> bool:
        logger.info("Проверка поля на обязательное")
        return locator.evaluate("el => !el.checkValidity()")