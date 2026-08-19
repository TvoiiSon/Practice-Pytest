import pytest
import allure
from playwright.sync_api import Page, expect
from pages.news_feed_page import NewsFeedPage
from pages.article_page import ArticlePage
from models.article import Article
from loguru import logger

@allure.severity(allure.severity_level.NORMAL)
@allure.tag("Позитивный")
@pytest.mark.smoke
@pytest.mark.ui
def test_correct_count_news(page: Page):
    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()

    expect(news_feed_page.list_articles).to_have_count(10)

@allure.severity(allure.severity_level.NORMAL)
@allure.tag("Позитивный")
@pytest.mark.smoke
@pytest.mark.ui
def test_correct_sorted_news(page: Page):
    with allure.step("Запрос списка новостей: page=1, per_page=10 — проверка сортировки по created_at"):
        logger.info("Запрос списка новостей: page=1, per_page=10 — проверка сортировки по created_at")
        request = page.request.get(f"https://archiscope.ru/api/news/?page=1&per_page=10").json()
        items = []
        for item in request["items"]:
            items.append(item["created_at"])

        assert items == sorted(items, reverse=True)

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("Позитивный")
@pytest.mark.smoke
@pytest.mark.ui
def test_correct_redirect_article(page: Page):
    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()

    title_article = news_feed_page.list_articles.first.text_content()

    news_feed_page.open_article(title_article)
    article_page = ArticlePage(page, title_article)

    expect(article_page.heading).to_be_visible()

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("Позитивный")
@pytest.mark.api
def test_correct_answer_api_article(page: Page):
    with allure.step("Запрос одной новости: page=1, per_page=1 — проверка схемы через Pydantic-модель Article"):
        logger.info("Запрос одной новости: page=1, per_page=1 — проверка схемы через Pydantic-модель Article")
        request = page.request.get("https://archiscope.ru/api/news/?page=1&per_page=1").json()

        assert Article(**request["items"][0])

@allure.severity(allure.severity_level.MINOR)
@allure.tag("Негативный")
@pytest.mark.parametrize("params_page", [-1, 0])
@pytest.mark.api
def test_incorrect_page_api_article(page: Page, params_page):
    with allure.step(f"Запрос списка новостей с невалидным page={params_page} — ожидаем 422"):
        logger.info(f"Запрос списка новостей с невалидным page={params_page} — ожидаем 422")
        request = page.request.get(f"https://archiscope.ru/api/news/?page={params_page}&per_page=10")

        assert request.status == 422

@allure.severity(allure.severity_level.MINOR)
@allure.tag("Негативный")
@pytest.mark.parametrize("params_page", [9999])
@pytest.mark.api
def test_incorrect_page_api_article_empty(page: Page, params_page):
    with allure.step(f"Запрос списка новостей за пределами доступных страниц page={params_page} — ожидаем 200 и пустой items"):
        logger.info(f"Запрос списка новостей за пределами доступных страниц page={params_page} — ожидаем 200 и пустой items")
        request = page.request.get(f"https://archiscope.ru/api/news/?page={params_page}&per_page=10")
        answer = request.json()
        assert answer["items"] == [] and request.status == 200

@allure.severity(allure.severity_level.MINOR)
@allure.tag("Негативный")
@pytest.mark.parametrize("params_per_page", [-1, 0, 9999])
@pytest.mark.api
def test_incorrect_per_page_api_article(page: Page, params_per_page):
    with allure.step(f"Запрос списка новостей с невалидным per_page={params_per_page} — ожидаем 422"):
        logger.info(f"Запрос списка новостей с невалидным per_page={params_per_page} — ожидаем 422")
        request = page.request.get(f"https://archiscope.ru/api/news/?page=1&per_page={params_per_page}")

        assert request.status == 422

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("Позитивный")
@pytest.mark.smoke
@pytest.mark.ui
def test_correct_change_content(page: Page):
    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()
    expect(news_feed_page.list_articles).to_have_count(10)

    title_article_first = news_feed_page.list_articles.first.text_content()

    news_feed_page.go_to_page("2")

    try:
        expect(news_feed_page.list_articles.first).not_to_have_text(title_article_first, timeout=1000)
    except AssertionError as e:
        logger.warning("Известный баг: клик по пагинации перекрыт фоновым self-refetch, повтор клика")
        news_feed_page.go_to_page("2")
        expect(news_feed_page.list_articles.first).not_to_have_text(title_article_first)

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("Позитивный")
@pytest.mark.smoke
@pytest.mark.ui
def test_correct_return_to_first_page(page: Page):
    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()
    expect(news_feed_page.list_articles).to_have_count(10)

    title_article_first = news_feed_page.list_articles.first.text_content()
    news_feed_page.go_to_page("2")

    try:
        expect(news_feed_page.list_articles.first).not_to_have_text(title_article_first)
    except AssertionError as e:
            logger.warning("Известный баг: клик по пагинации перекрыт фоновым self-refetch, повтор клика")
            news_feed_page.go_to_page("2")
            expect(news_feed_page.list_articles.first).not_to_have_text(title_article_first)

    news_feed_page.go_to_page("1")

    try:
        expect(news_feed_page.list_articles.first).to_have_text(title_article_first)
    except AssertionError as e:
            logger.warning("Известный баг: клик по пагинации перекрыт фоновым self-refetch, повтор клика")
            news_feed_page.go_to_page("1")
            expect(news_feed_page.list_articles.first).to_have_text(title_article_first)

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("Позитивный")
@pytest.mark.smoke
@pytest.mark.ui
def test_correct_change_content_api(page: Page):
    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()
    expect(news_feed_page.list_articles).to_have_count(10)

    title_article_first = news_feed_page.list_articles.first.text_content()
    with allure.step("Запрос страницы 1 через API — сверка с тем, что показывает UI"):
        logger.info("Запрос страницы 1 через API — сверка с тем, что показывает UI")
        request = page.request.get("https://archiscope.ru/api/news/?page=1&per_page=10").json()
        assert request["items"][0]["title"] == title_article_first

    
    news_feed_page.go_to_page("2")

    try:
        expect(news_feed_page.list_articles.first).not_to_have_text(title_article_first)
    except AssertionError as e:
            logger.warning("Известный баг: клик по пагинации перекрыт фоновым self-refetch, повтор клика")
            news_feed_page.go_to_page("2")
            expect(news_feed_page.list_articles.first).not_to_have_text(title_article_first)

    title_article_second = news_feed_page.list_articles.first.text_content()
    with allure.step("Запрос страницы 2 через API — сверка с тем, что показывает UI"):
        logger.info("Запрос страницы 2 через API — сверка с тем, что показывает UI")
        request_s = page.request.get("https://archiscope.ru/api/news/?page=2&per_page=10").json()
        assert request_s["items"][0]["title"] == title_article_second

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("Позитивный")
@pytest.mark.smoke
@pytest.mark.ui
def test_correct_search_article(page: Page):
    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()
    expect(news_feed_page.list_articles).to_have_count(10)

    title_before_search = news_feed_page.list_articles.first.text_content()
    _ = news_feed_page.search(title_before_search)
    title_after_search = news_feed_page.list_articles.first.text_content()

    assert title_before_search == title_after_search

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("Негативный")
@pytest.mark.smoke
@pytest.mark.ui
def test_incorrect_search_article(page: Page):
    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()
    expect(news_feed_page.list_articles).to_have_count(10)

    news_feed_page.search("asdkfjhqwerty12345")

    expect(news_feed_page.notfound_text).to_be_visible()

@allure.severity(allure.severity_level.NORMAL)
@allure.tag("Позитивный")
@pytest.mark.smoke
@pytest.mark.ui
def test_correct_clear_search_article(page: Page):
    news_feed_page = NewsFeedPage(page)
    news_feed_page.open()
    expect(news_feed_page.list_articles).to_have_count(10)

    title_before_search = news_feed_page.list_articles.first.text_content()
    news_feed_page.search(title_before_search)

    news_feed_page.clear_search()

    expect(news_feed_page.list_articles).to_have_count(10)

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("Негативный")
@pytest.mark.api
def test_no_pii_leak_api_article(page: Page):
    with allure.step("Запрос списка новостей — проверка отсутствия email/phone автора в ответе"):
        logger.info("Запрос списка новостей — проверка отсутствия email/phone автора в ответе")
        request = page.request.get("https://archiscope.ru/api/news/?page=1&per_page=1").json()

        for item in request["items"]:
            assert "email" not in item["author"] and "phone" not in item["author"]
