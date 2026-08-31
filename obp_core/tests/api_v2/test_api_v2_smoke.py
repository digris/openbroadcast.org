import pytest
from django.core.urlresolvers import reverse


pytestmark = pytest.mark.django_db


def test_v2_api_root_accepts_authenticated_get(client, admin_user):
    client.force_login(admin_user)

    response = client.get("/api/v2/")

    assert response.status_code == 200


@pytest.mark.parametrize(
    "url_name",
    [
        "api:emission-list",
        "api:artist-list",
        "api:playlist-list",
        "api:profile-list",
        "api:export-list",
        "api:search-index",
        "api:collector-index",
    ],
)
def test_v2_registered_list_and_root_endpoints_accept_authenticated_get(
    client, admin_user, url_name
):
    client.force_login(admin_user)

    response = client.get(reverse(url_name))

    assert response.status_code == 200
