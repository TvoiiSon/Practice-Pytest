import pytest
from playwright.sync_api import Page, expect
from pages.create_news_page import CreateNewsPage
from pages.login_page import LoginPage
from helpers.data_generator import generate_article
from config import BASE_URL

@pytest.mark.smoke
def test_correct_create_article(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("test@example.com", "password123")

    expect(login_page.header.avatar_button).to_be_visible()
    assert page.evaluate("localStorage.getItem('token')")

    create_new_article_page = CreateNewsPage(page)
    create_new_article_page.open()

    article = generate_article()

    with page.expect_response("**/api/news/*") as response_info:
        create_new_article_page.create_news(**article)
    response = response_info.value

    assert response.status == 200
    expect(page.get_by_text(article["title"])).to_be_visible()

@pytest.mark.regression
def test_create_article_with_image(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("test@example.com", "password123")

    expect(login_page.header.avatar_button).to_be_visible()
    assert page.evaluate("localStorage.getItem('token')")

    create_new_article_page = CreateNewsPage(page)
    create_new_article_page.open()

    article = generate_article()
    create_new_article_page.create_news(**article, image_path="test_data/images.jpeg")

    request = page.request.get("https://archiscope.ru/api/news").json()
    image_path = ""
    for item in request["items"]:
        if item["title"] == article["title"]:
            image_path = item["image_path"]

    second_request = page.request.get(BASE_URL + image_path)
    assert second_request.status == 200
    
@pytest.mark.parametrize("empty_field", ["title", "text"])
@pytest.mark.regression
def test_empty_required_field(page: Page, empty_field):
    login_page = LoginPage(page)
    login_page.open()

    login_page.login("test@example.com", "password123")

    expect(login_page.header.avatar_button).to_be_visible()
    assert page.evaluate("localStorage.getItem('token')")

    create_new_article_page = CreateNewsPage(page)
    create_new_article_page.open()

    article = generate_article()
    article[empty_field] = ""

    create_new_article_page.create_news(**article, image_path="test_data/images.jpeg")

    validate_locator = getattr(create_new_article_page, f"{empty_field}_input")
    assert create_new_article_page.is_field_required(validate_locator)

@pytest.mark.parametrize("empty_field", ["subtitle", "tags"])
@pytest.mark.regression
def test_empty_notrequired_field(page: Page, empty_field):
    login_page = LoginPage(page)
    login_page.open()

    login_page.login("test@example.com", "password123")

    expect(login_page.header.avatar_button).to_be_visible()
    assert page.evaluate("localStorage.getItem('token')")

    create_new_article_page = CreateNewsPage(page)
    create_new_article_page.open()

    article = generate_article()
    article[empty_field] = ""

    with page.expect_response("**/api/news/*") as response_info:
        create_new_article_page.create_news(**article)
    response = response_info.value

    assert response.status == 200
    expect(page.get_by_text(article["title"])).to_be_visible()
    