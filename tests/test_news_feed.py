import pytest
from playwright.sync_api import Page, expect
from pages.news_feed_page import NewsFeedPage
from pages.article_page import ArticlePage

@pytest.mark.regression
def test_correct_count_news(page: Page):
    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()

    expect(news_feed_page.list_articles).to_have_count(10)

@pytest.mark.regression
def test_correct_sorted_news(page: Page):
    request = page.request.get(f"https://archiscope.ru/api/news/?page=1&per_page=10").json()
    items = []
    for item in request["items"]:
        items.append(item["created_at"])

    assert items == sorted(items, reverse=True) 

@pytest.mark.regression
def test_correct_redirect_article(page: Page):
    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()

    title_article = news_feed_page.list_articles.first.text_content()

    news_feed_page.open_article(title_article)
    article_page = ArticlePage(page, title_article)

    expect(article_page.heading).to_be_visible()
