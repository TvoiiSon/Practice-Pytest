import pytest
from playwright.sync_api import Page, expect
from pages.header_component import HeaderComponent
from pages.profile_page import ProfilePage
from helpers.data_generator import generate_user
from config import BASE_URL

@pytest.mark.smoke
def test_valid_update_profile(go_to_profile_page: ProfilePage):
    for_profile = generate_user()
    go_to_profile_page.update_profile(**for_profile)
    expect(go_to_profile_page.page.get_by_text("Профиль обновлён")).to_be_visible()

@pytest.mark.regression
def test_update_profile_with_set_photo(go_to_profile_page: ProfilePage):
    for_profile = generate_user()
    go_to_profile_page.update_profile(**for_profile, image_path="test_data/images.jpeg")

    token = go_to_profile_page.page.evaluate("localStorage.getItem('token')")
    request = go_to_profile_page.page.request.get("https://archiscope.ru/api/users/me", headers={'Authorization': f'Bearer {token}'}).json()

    second_request = go_to_profile_page.page.request.get(BASE_URL + request["photo_path"])
    assert second_request.status == 200

@pytest.mark.parametrize("empty_field", ["first_name", "last_name", "email"])
@pytest.mark.regression
def test_update_profile_without_required_fields(go_to_profile_page: ProfilePage, empty_field):
    for_profile = generate_user()
    for_profile[empty_field] = ""
    go_to_profile_page.update_profile(**for_profile)
    validate_locator = getattr(go_to_profile_page, f"{empty_field}_input")
    assert go_to_profile_page.is_field_required(validate_locator)

@pytest.mark.parametrize("empty_field", ["phone", "password", "image_path"])
@pytest.mark.regression
def test_update_profile_without_notrequired_fields(go_to_profile_page: ProfilePage, empty_field):
    for_profile = generate_user()
    if empty_field != "image_path":
        for_profile[empty_field] = ""
    go_to_profile_page.update_profile(**for_profile)
    expect(go_to_profile_page.page.get_by_text("Профиль обновлён")).to_be_visible()
