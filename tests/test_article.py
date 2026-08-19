import pytest
import allure
from playwright.sync_api import Page, expect
from pages.article_page import ArticlePage
from models.article import Comment
from helpers.data_generator import generate_comment

@allure.tag("Позитивный")
@pytest.mark.smoke
def test_correct_create_comment(go_to_article_page: ArticlePage):
    comment = generate_comment()
    go_to_article_page.add_comment(comment)

    expect(go_to_article_page.page.locator("p").get_by_text(comment)).to_be_visible()

@allure.tag("Негативный")
@pytest.mark.regression
def test_incorrect_create_comment(go_to_article_page: ArticlePage):
    go_to_article_page.add_comment("")
    assert go_to_article_page.is_field_required(go_to_article_page.comment_input)

@allure.tag("Негативный")
@pytest.mark.api
def test_pii_article_id_returns(page: Page):
    request = page.request.get("https://archiscope.ru/api/news/39/comments").json()

    for item in request:
        assert "email" not in item["author"] and "phone" not in item["author"]

@allure.tag("Позитивный")
@pytest.mark.api
def test_valid_article_id_returns(page: Page):
    request = page.request.get("https://archiscope.ru/api/news/39/comments").json()
    for item in request:
        assert Comment(**item)

@allure.tag("Негативный")
@pytest.mark.parametrize("article_id", [-1, 0, 9999])
@pytest.mark.api
def test_invalid_article_id_returns_404(page: Page, article_id):
    request = page.request.get(f"https://archiscope.ru/api/news/{article_id}/comments")
    assert request.status == 404
