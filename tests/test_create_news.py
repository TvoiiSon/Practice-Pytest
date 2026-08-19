import pytest
import allure
from playwright.sync_api import Page, expect
from pages.create_news_page import CreateNewsPage
from helpers.data_generator import generate_article
from config import BASE_URL

@allure.tag("Позитивный")
@pytest.mark.smoke
def test_correct_create_article(go_to_create_news_page: CreateNewsPage):
    article = generate_article()

    with go_to_create_news_page.page.expect_response("**/api/news/*") as response_info:
        go_to_create_news_page.create_news(**article)
    response = response_info.value

    assert response.status == 200
    expect(go_to_create_news_page.page.get_by_text(article["title"])).to_be_visible()

@allure.tag("Позитивный")
@pytest.mark.regression
def test_create_article_with_image(go_to_create_news_page: CreateNewsPage):
    article = generate_article()
    go_to_create_news_page.create_news(**article, image_path="test_data/images.jpeg")

    request = go_to_create_news_page.page.request.get("https://archiscope.ru/api/news").json()
    image_path = ""
    for item in request["items"]:
        if item["title"] == article["title"]:
            image_path = item["image_path"]

    second_request = go_to_create_news_page.page.request.get(BASE_URL + image_path)
    assert second_request.status == 200

@allure.tag("Негативный")
@pytest.mark.parametrize("empty_field", ["title", "text"])
@pytest.mark.regression
def test_empty_required_field(go_to_create_news_page: CreateNewsPage, empty_field):
    article = generate_article()
    article[empty_field] = ""

    go_to_create_news_page.create_news(**article, image_path="test_data/images.jpeg")

    validate_locator = getattr(go_to_create_news_page, f"{empty_field}_input")
    assert go_to_create_news_page.is_field_required(validate_locator)

@allure.tag("Позитивный")
@pytest.mark.parametrize("empty_field", ["subtitle", "tags"])
@pytest.mark.regression
def test_empty_notrequired_field(go_to_create_news_page: CreateNewsPage, empty_field):
    article = generate_article()
    article[empty_field] = ""

    with go_to_create_news_page.page.expect_response("**/api/news/*") as response_info:
        go_to_create_news_page.create_news(**article)
    response = response_info.value

    assert response.status == 200
    expect(go_to_create_news_page.page.get_by_text(article["title"])).to_be_visible()
