from playwright.sync_api import Page
from pages.base_page import BasePage
from config import BASE_URL
from loguru import logger

class CreateNewsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title_input = page.locator('input[name="title"]')
        self.subtitle_input = page.locator('input[name="subtitle"]')
        self.text_input = page.locator('textarea[name="text"]')
        self.tags_input = page.get_by_role("textbox", name="технологии, наука, спорт")
        self.image_input = page.locator('input[type="file"]')
        self.create_button = page.get_by_role("button", name="Создать")

    def create_news(self, title: str, text: str, subtitle: str = "", tags: str = "", image_path: str = ""):
        self.title_input.fill(title)
        self.text_input.fill(text)
        if subtitle:
            self.subtitle_input.fill(subtitle)
        if tags:
            self.tags_input.fill(tags)
        if image_path:
            self.image_input.set_input_files(image_path)
        logger.info(f"Создание новости с Названием: {title}")
        self.create_button.click()

    def open(self):
        logger.info("Переход на страницу создания новости")
        self.page.goto(BASE_URL + "/news/create")

    def is_field_required(self, locator) -> bool:
        logger.info("Проверка поля на обязательное")
        return locator.evaluate("el => !el.checkValidity()")
    