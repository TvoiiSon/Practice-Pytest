import re
from playwright.sync_api import Page

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

    def open_profile(self):
        self.avatar_button.click()
        self.profile_link.click()

    def logout(self):
        self.avatar_button.click()
        self.logout_button.click()
