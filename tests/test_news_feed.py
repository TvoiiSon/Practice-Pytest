import pytest
from playwright.sync_api import Page, expect
from pages.news_feed_page import NewsFeedPage

@pytest.mark.regression
def test_count_news_feed(page: Page):
    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()

    expect(news_feed_page.list_articles).to_have_count(10)
