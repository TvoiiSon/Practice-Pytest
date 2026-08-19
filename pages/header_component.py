import re
import allure
from playwright.sync_api import Page
from loguru import logger

class HeaderComponent:
    def __init__(self, page: Page):
        self.page = page
        self.logo_link = page.get_by_role("link", name="📰 NewsPlatform")
        self.login_link = page.get_by_role("link", name="Войти")
        self.register_link = page.get_by_role("link", name="Регистрация")
        self.add_news_link = page.get_by_role("link", name="+ Добавить новость")
        self.avatar_button = page.get_by_role("button", name=re.compile(r"^[A-ZА-Я]$"))
        self.profile_link = page.get_by_role("link", name="Профиль")
        self.logout_button = page.get_by_role("button", name="Выйти")

    @allure.step("Переход на страницу Профиля через нажатие по аватару, затем кнопке Профиль")
    def open_profile(self):
        logger.info("Переход на страницу Профиля через нажатие по аватару, затем кнопке Профиль")
        self.avatar_button.click()
        self.profile_link.click()

    @allure.step("Выход из аккаунта пользователя через нажатие по аватару, затем кнопке Выйти")
    def logout(self):
        logger.info("Выход из аккаунта пользователя через нажатие по аватару, затем кнопке Выйти")
        self.avatar_button.click()
        self.logout_button.click()
