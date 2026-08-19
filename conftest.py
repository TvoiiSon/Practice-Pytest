import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.news_feed_page import NewsFeedPage
from pages.article_page import ArticlePage
from pages.create_news_page import CreateNewsPage
from pages.profile_page import ProfilePage
from pages.header_component import HeaderComponent
from helpers.data_generator import generate_user
from config import BASE_URL

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
    }

@pytest.fixture
def authenticated_page(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("test@example.com", "password123")
    expect(login_page.header.avatar_button).to_be_visible()
    assert page.evaluate("localStorage.getItem('token')")

    return page

@pytest.fixture
def register_page(page: Page):
    register_page = RegisterPage(page)
    register_page.open()
    generated_user = generate_user()
    register_page.register(**generated_user)
    expect(page).to_have_url(BASE_URL + "/login")

    login_page = LoginPage(page)
    login_page.login(generated_user["email"], generated_user["password"])
    expect(login_page.header.avatar_button).to_be_visible()
    assert page.evaluate("localStorage.getItem('token')")

    return page

@pytest.fixture
def go_to_article_page(authenticated_page: Page):
    news_feed_page = NewsFeedPage(authenticated_page)
    news_feed_page.open()

    title_article = news_feed_page.list_articles.first.text_content()
    
    news_feed_page.open_article(title_article)
    article_page = ArticlePage(authenticated_page, title_article)
    expect(article_page.heading).to_be_visible()

    return article_page

@pytest.fixture
def go_to_create_news_page(authenticated_page: Page):
    create_new_article_page = CreateNewsPage(authenticated_page)
    create_new_article_page.open()
    expect(authenticated_page).to_have_url(BASE_URL + "/news/create")

    return create_new_article_page

@pytest.fixture
def go_to_profile_page(register_page: Page):
    header = HeaderComponent(register_page)
    header.open_profile()
    expect(register_page).to_have_url(BASE_URL + "/profile")

    profile_page = ProfilePage(register_page)
    
    return profile_page
