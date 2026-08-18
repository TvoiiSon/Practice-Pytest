import pytest
from playwright.sync_api import Page, expect
from pages.news_feed_page import NewsFeedPage

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
