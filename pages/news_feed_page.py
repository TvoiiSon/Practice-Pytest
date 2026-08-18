from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.create_news_page import CreateNewsPage
from config import BASE_URL

class NewsFeedPage(BasePage):
    URL = BASE_URL

    def __init__(self, page: Page):
        super().__init__(page)
        self.logo_link = page.get_by_role("link", name="📰 NewsPlatform")
        self.login_link = page.get_by_role("link", name="Войти")
        self.register_link = page.get_by_role("link", name="Регистрация")
        self.list_articles = page.get_by_role("heading", level=2)
        self.add_news_link = page.get_by_role("link", name="+ Добавить новость")
        self.search_input = page.get_by_role("textbox", name="Поиск")
        self.clear_search_button = page.get_by_role("button", name="Очистить поиск")
        self.notfound_text = page.get_by_text("Ничего не найдено")
        self.next_page_button = page.get_by_role("button", name="»")
        self.prev_page_button = page.get_by_role("button", name="«")

    def open(self):
        self.page.goto(self.URL)

    def search(self, query: str):
        self.search_input.fill(query)

    def clear_search(self):
        self.clear_search_button.click()

    def open_article(self, title: str):
        self.page.get_by_role("link", name=title).click()

    def go_to_page(self, number: str):
        self.page.get_by_role("button", name=number).click()

    def open_create_news_page(self) -> CreateNewsPage:
        with self.page.expect_popup() as popup_info:
            self.add_news_link.click()
        return CreateNewsPage(popup_info.value)
