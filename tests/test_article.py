import pytest
from playwright.sync_api import Page, expect
from pages.article_page import ArticlePage
from pages.login_page import LoginPage
from pages.news_feed_page import NewsFeedPage
from models.article import Comment
from helpers.data_generator import generate_comment

@pytest.mark.smoke
def test_correct_create_comment(page: Page):
    login_page = LoginPage(page)
    login_page.open()

    login_page.login("test@example.com", "password123")

    expect(login_page.header.avatar_button).to_be_visible()
    assert page.evaluate("localStorage.getItem('token')")

    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()

    title_article = news_feed_page.list_articles.first.text_content()
    
    news_feed_page.open_article(title_article)
    article_page = ArticlePage(page, title_article)

    comment = generate_comment()
    article_page.add_comment(comment)

    expect(page.locator("p").get_by_text(comment)).to_be_visible()

@pytest.mark.regression
def test_incorrect_create_comment(page: Page):
    login_page = LoginPage(page)
    login_page.open()

    login_page.login("test@example.com", "password123")

    expect(login_page.header.avatar_button).to_be_visible()
    assert page.evaluate("localStorage.getItem('token')")

    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()

    title_article = news_feed_page.list_articles.first.text_content()
    
    news_feed_page.open_article(title_article)
    article_page = ArticlePage(page, title_article)

    article_page.add_comment("")
    assert article_page.is_field_required(article_page.comment_input)

@pytest.mark.api
def test_pii_article_id_returns(page: Page):
    request = page.request.get("https://archiscope.ru/api/news/39/comments").json()

    for item in request:
        assert "email" not in item["author"] and "phone" not in item["author"]

@pytest.mark.api
def test_valid_article_id_returns(page: Page):
    request = page.request.get("https://archiscope.ru/api/news/39/comments").json()
    for item in request:
        assert Comment(**item)

@pytest.mark.parametrize("article_id", [-1, 0, 9999])
@pytest.mark.api
def test_invalid_article_id_returns_404(page: Page, article_id):
    request = page.request.get(f"https://archiscope.ru/api/news/{article_id}/comments")
    assert request.status == 404
