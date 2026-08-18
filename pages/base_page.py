from playwright.sync_api import Page
from pages.header_component import HeaderComponent

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.header = HeaderComponent(page)

    def get_title(self) -> str:
        return self.page.title()
