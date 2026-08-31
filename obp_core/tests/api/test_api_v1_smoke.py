import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url",
    [
        # "/api/v1/abcast/base/",
        "/api/v1/abcast/emission/",
        "/api/v1/library/artist/",
        "/api/v1/library/release/",
        "/api/v1/library/track/",
        "/api/v1/library/playlist/",
        "/api/v1/rating/vote/",
        "/api/v1/library/release/schema/",
    ],
)
def test_api_endpoints_authenticated(client, admin_user, url):
    client.force_login(admin_user)

    response = client.get(url)

    assert response.status_code == 200
