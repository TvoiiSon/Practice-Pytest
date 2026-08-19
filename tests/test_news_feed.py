import pytest
from playwright.sync_api import Page, expect
from pages.news_feed_page import NewsFeedPage
from pages.article_page import ArticlePage
from models.article import Article

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

@pytest.mark.api
def test_correct_answer_api_article(page: Page):
    request = page.request.get("https://archiscope.ru/api/news/?page=1&per_page=1").json()
    
    assert Article(**request["items"][0])

@pytest.mark.parametrize("params_page", [-1, 0])
@pytest.mark.api
def test_incorrect_page_api_article(page: Page, params_page):
    request = page.request.get(f"https://archiscope.ru/api/news/?page={params_page}&per_page=10")

    assert request.status == 422


@pytest.mark.parametrize("params_page", [9999])
@pytest.mark.api
def test_incorrect_page_api_article_empty(page: Page, params_page):
    request = page.request.get(f"https://archiscope.ru/api/news/?page={params_page}&per_page=10")
    answer = request.json()
    assert answer["items"] == [] and request.status == 200

@pytest.mark.parametrize("params_per_page", [-1, 0, 9999])
@pytest.mark.api
def test_incorrect_per_page_api_article(page: Page, params_per_page):
    request = page.request.get(f"https://archiscope.ru/api/news/?page=1&per_page={params_per_page}")

    assert request.status == 422

@pytest.mark.regression
def test_correct_change_content(page: Page):
    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()
    expect(news_feed_page.list_articles).to_have_count(10)

    title_article_first = news_feed_page.list_articles.first.text_content()

    page.wait_for_timeout(1000)

    news_feed_page.go_to_page("2")

    expect(news_feed_page.list_articles.first).not_to_have_text(title_article_first)

@pytest.mark.regression
def test_correct_return_to_first_page(page: Page):
    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()
    expect(news_feed_page.list_articles).to_have_count(10)

    title_article_first = news_feed_page.list_articles.first.text_content()
    page.wait_for_timeout(1000)
    news_feed_page.go_to_page("2")
    page.wait_for_timeout(1000)
    expect(news_feed_page.list_articles.first).not_to_have_text(title_article_first)

    page.wait_for_timeout(1000)
    news_feed_page.go_to_page("1")
    page.wait_for_timeout(1000)

    expect(news_feed_page.list_articles.first).to_have_text(title_article_first)

@pytest.mark.regression
def test_correct_change_content_api(page: Page):
    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()
    expect(news_feed_page.list_articles).to_have_count(10)
    
    title_article_first = news_feed_page.list_articles.first.text_content()
    request = page.request.get("https://archiscope.ru/api/news/?page=1&per_page=10").json()
    assert request["items"][0]["title"] == title_article_first

    page.wait_for_timeout(1000)
    news_feed_page.go_to_page("2")
    page.wait_for_timeout(1000)

    title_article_second = news_feed_page.list_articles.first.text_content()
    request_s = page.request.get("https://archiscope.ru/api/news/?page=2&per_page=10").json()
    assert request_s["items"][0]["title"] == title_article_second

@pytest.mark.regression
def test_correct_search_article(page: Page):
    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()
    expect(news_feed_page.list_articles).to_have_count(10)
        
    title_before_search = news_feed_page.list_articles.first.text_content()
    _ = news_feed_page.search(title_before_search)
    page.wait_for_timeout(1000)
    title_after_search = news_feed_page.list_articles.first.text_content()

    assert title_before_search == title_after_search

@pytest.mark.regression
def test_incorrect_search_article(page: Page):
    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()
    expect(news_feed_page.list_articles).to_have_count(10)
    
    _ = news_feed_page.search("asdkfjhqwerty12345")
    page.wait_for_timeout(1000)

    expect(news_feed_page.notfound_text).to_be_visible()

@pytest.mark.regression
def test_correct_clear_search_article(page: Page):
    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()
    expect(news_feed_page.list_articles).to_have_count(10)
        
    title_before_search = news_feed_page.list_articles.first.text_content()
    _ = news_feed_page.search(title_before_search)
    page.wait_for_timeout(1000)

    news_feed_page.clear_search()

    expect(news_feed_page.list_articles).to_have_count(10)

@pytest.mark.api
def test_no_pii_leak_api_article(page: Page):
    request = page.request.get("https://archiscope.ru/api/news/?page=1&per_page=1").json()

    for item in request["items"]:
        assert "email" not in item["author"] and "phone" not in item["author"]
