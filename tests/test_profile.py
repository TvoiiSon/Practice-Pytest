import pytest
from playwright.sync_api import Page, expect
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from pages.header_component import HeaderComponent
from pages.profile_page import ProfilePage
from helpers.data_generator import generate_user
from config import BASE_URL

@pytest.mark.smoke
def test_valid_update_profile(page: Page):
    register_page = RegisterPage(page)
    register_page.open()
    generated_user = generate_user()
    register_page.register(**generated_user)
    expect(page).to_have_url(BASE_URL + "/login")

    login_page = LoginPage(page)
    login_page.login(generated_user["email"], generated_user["password"])
    expect(login_page.header.avatar_button).to_be_visible()
    assert page.evaluate("localStorage.getItem('token')")

    header = HeaderComponent(page)
    header.open_profile()
    expect(page).to_have_url(BASE_URL + "/profile")

    profile_page = ProfilePage(page)
    for_profile = generate_user()
    profile_page.update_profile(**for_profile)
    expect(page.get_by_text("Профиль обновлён")).to_be_visible()

@pytest.mark.regression
def test_update_profile_with_set_photo(page: Page):
    register_page = RegisterPage(page)
    register_page.open()
    generated_user = generate_user()
    register_page.register(**generated_user)
    expect(page).to_have_url(BASE_URL + "/login")

    login_page = LoginPage(page)
    login_page.login(generated_user["email"], generated_user["password"])
    expect(login_page.header.avatar_button).to_be_visible()
    token = page.evaluate("localStorage.getItem('token')")
    assert token

    header = HeaderComponent(page)
    header.open_profile()
    expect(page).to_have_url(BASE_URL + "/profile")

    profile_page = ProfilePage(page)
    for_profile = generate_user()
    profile_page.update_profile(**for_profile, image_path="test_data/images.jpeg")

    request = page.request.get("https://archiscope.ru/api/users/me", headers={'Authorization': f'Bearer {token}'}).json()

    second_request = page.request.get(BASE_URL + request["photo_path"])
    assert second_request.status == 200

@pytest.mark.parametrize("empty_field", ["first_name", "last_name", "email"])
@pytest.mark.regression
def test_update_profile_without_required_fields(page: Page, empty_field):
    register_page = RegisterPage(page)
    register_page.open()
    generated_user = generate_user()
    register_page.register(**generated_user)
    expect(page).to_have_url(BASE_URL + "/login")

    login_page = LoginPage(page)
    login_page.login(generated_user["email"], generated_user["password"])
    expect(login_page.header.avatar_button).to_be_visible()
    assert page.evaluate("localStorage.getItem('token')")

    header = HeaderComponent(page)
    header.open_profile()
    expect(page).to_have_url(BASE_URL + "/profile")

    profile_page = ProfilePage(page)
    for_profile = generate_user()
    for_profile[empty_field] = ""
    profile_page.update_profile(**for_profile)
    validate_locator = getattr(profile_page, f"{empty_field}_input")
    assert profile_page.is_field_required(validate_locator)

@pytest.mark.parametrize("empty_field", ["phone", "password", "image_path"])
@pytest.mark.regression
def test_update_profile_without_notrequired_fields(page: Page, empty_field):
    register_page = RegisterPage(page)
    register_page.open()
    generated_user = generate_user()
    register_page.register(**generated_user)
    expect(page).to_have_url(BASE_URL + "/login")

    login_page = LoginPage(page)
    login_page.login(generated_user["email"], generated_user["password"])
    expect(login_page.header.avatar_button).to_be_visible()
    assert page.evaluate("localStorage.getItem('token')")

    header = HeaderComponent(page)
    header.open_profile()
    expect(page).to_have_url(BASE_URL + "/profile")

    profile_page = ProfilePage(page)
    for_profile = generate_user()
    if empty_field != "image_path":
        for_profile[empty_field] = ""
    profile_page.update_profile(**for_profile)
    expect(page.get_by_text("Профиль обновлён")).to_be_visible()
