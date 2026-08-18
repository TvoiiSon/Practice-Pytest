from playwright.sync_api import Page
from pages.base_page import BasePage

class ArticlePage(BasePage):
    def __init__(self, page: Page, title: str = None):
        super().__init__(page)
        self.comment_input = page.get_by_role("textbox", name="Оставьте комментарий")
        self.submit_comment_button = page.get_by_role("button", name="Отправить")
        self.heading = page.get_by_role("heading", name=title)

    def add_comment(self, text: str):
        self.comment_input.fill(text)
        self.submit_comment_button.click()
