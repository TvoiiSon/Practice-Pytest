from playwright.sync_api import Page
from pages.base_page import BasePage

class CreateNewsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title_input = page.locator('input[name="title"]')
        self.subtitle_input = page.locator('input[name="subtitle"]')
        self.text_input = page.locator('textarea[name="text"]')
        self.tags_input = page.get_by_role("textbox", name="технологии, наука, спорт")
        self.create_button = page.get_by_role("button", name="Создать")

    def create_news(self, title: str, text: str, subtitle: str = "", tags: str = ""):
        self.title_input.fill(title)
        self.text_input.fill(text)
        if subtitle:
            self.subtitle_input.fill(subtitle)
        if tags:
            self.tags_input.fill(tags)
        self.create_button.click()
