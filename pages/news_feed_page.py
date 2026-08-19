import allure
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from pages.base_page import BasePage
from pages.create_news_page import CreateNewsPage
from config import BASE_URL
from loguru import logger

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
        with self.page.expect_response(lambda r: "/api/news/?page=1" in r.url):
            self.page.goto(self.URL)
        try:
            with self.page.expect_response(lambda r: "/api/news/?page=1" in r.url, timeout=1000):
                pass
            logger.warning("Известный баг: пойман фоновый повторный запрос page=1 после загрузки ленты")
        except PlaywrightTimeoutError:
            pass

    @allure.step("Поиск новости с Названием: {query}")
    def search(self, query: str):
        logger.info(f"Поиск новости с Названием: {query}")
        self.search_input.fill(query)

    @allure.step("Нажатие на кнопку очистки формы поиска")
    def clear_search(self):
        logger.info("Нажатие на кнопку очистки формы поиска")
        self.clear_search_button.click()

    @allure.step("Переход на страницу новости, по нажатию на ссылку в Названии: {title}")
    def open_article(self, title: str):
        logger.info(f"Переход на страницу новости, по нажатию на ссылку в Названии: {title}")
        self.page.get_by_role("link", name=title).click()

    @allure.step("Переход на страницу пагинации №{number}")
    def go_to_page(self, number: str):
        logger.info(f"Переход на страницу пагинации №{number}")
        self.page.get_by_role("button", name=number).click()

    @allure.step("Переход на страницу создания новости")
    def open_create_news_page(self) -> CreateNewsPage:
        logger.info("Переход на страницу создания новости")
        with self.page.expect_popup() as popup_info:
            self.add_news_link.click()
        return CreateNewsPage(popup_info.value)
