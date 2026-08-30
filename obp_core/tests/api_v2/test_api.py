from uuid import uuid4

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.urlresolvers import resolve, reverse
from rest_framework.test import APIClient

from alibrary.models import Artist
from exporter.models import Export


pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def obr_sync_user():
    user = get_user_model().objects.create_user(username="obr-sync-reader")
    permission = Permission.objects.get(
        content_type__app_label="account",
        codename="view_obr_sync_api",
    )
    user.user_permissions.add(permission)
    return user


def assert_paginated_empty_response(response):
    assert response.status_code == 200
    assert response.data == {
        "count": 0,
        "next": None,
        "previous": None,
        "results": [],
    }


def test_api_root_is_public_and_versioned(api_client):
    path = "/api/v2/"
    match = resolve(path)

    assert match.func

    response = api_client.get(path)

    assert response.status_code == 200
    assert response.data == {"version": "0.2.0"}


@pytest.mark.parametrize(
    "url_name",
    [
        "api:artist-list",
        "api:label-list",
        "api:release-list",
        "api:media-list",
    ],
)
def test_catalog_list_endpoints_keep_their_paginated_contract(api_client, url_name):
    path = reverse(url_name)
    match = resolve(path)

    assert match.url_name == url_name.split(":")[-1]

    response = api_client.get(path)

    assert_paginated_empty_response(response)


def test_artist_detail_serializes_the_stable_identity_fields(api_client):
    artist = Artist.objects.create(name="API Test Artist", d_tags="")
    path = reverse("api:artist-detail", kwargs={"uuid": artist.uuid})

    response = api_client.get(path)

    assert response.status_code == 200
    assert response.data["id"] == artist.pk
    assert response.data["uuid"] == str(artist.uuid)
    assert response.data["name"] == artist.name
    assert response.data["ct"] == "alibrary.artist"
    assert response.data["url"].endswith(path)
    assert response.data["detail_url"] == artist.get_absolute_url()

    missing_response = api_client.get(
        reverse("api:artist-detail", kwargs={"uuid": uuid4()})
    )
    assert missing_response.status_code == 404


def test_profile_can_be_retrieved_by_uuid_and_legacy_user_id(api_client):
    user = get_user_model().objects.create_user(
        username="api-profile",
        first_name="API",
        last_name="Profile",
    )
    profile = user.profile
    uuid_path = reverse("api:profile-detail", kwargs={"uuid": profile.uuid})
    user_id_path = reverse(
        "api:profile-detail-by-userid",
        kwargs={"user_id": user.pk},
    )

    uuid_response = api_client.get(uuid_path)
    user_id_response = api_client.get(user_id_path)

    assert uuid_response.status_code == 200
    assert user_id_response.status_code == 200
    assert uuid_response.data == user_id_response.data
    assert uuid_response.data["uuid"] == str(profile.uuid)
    assert uuid_response.data["user_id"] == user.pk
    assert uuid_response.data["ct"] == "profiles.profile"


def test_emission_reads_are_public_but_writes_require_scheduler_permission(api_client):
    path = reverse("api:emission-list")

    assert_paginated_empty_response(api_client.get(path))

    anonymous_response = api_client.post(path, {}, format="json")
    user = get_user_model().objects.create_user(username="scheduler-reader")
    api_client.force_authenticate(user=user)
    authenticated_response = api_client.post(path, {}, format="json")

    assert anonymous_response.status_code == 401
    assert authenticated_response.status_code == 403
    assert authenticated_response.data["detail"] == "insufficient permission"


def test_export_list_is_limited_to_the_authenticated_user(api_client):
    user = get_user_model().objects.create_user(username="export-owner")
    other_user = get_user_model().objects.create_user(username="other-export-owner")
    own_export = Export.objects.create(user=user, filename="own.zip")
    Export.objects.create(user=other_user, filename="other.zip")
    api_client.force_authenticate(user=user)
    own_export.refresh_from_db()

    response = api_client.get(reverse("api:export-list"))

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["uuid"] == str(own_export.uuid)
    assert response.data["results"][0]["name"] == own_export.filename


def test_player_root_and_invalid_play_request_keep_their_response_contract(api_client):
    play_path = reverse("api:player-play")

    root_response = api_client.get(reverse("api:player-index"))
    invalid_response = api_client.put(play_path, {}, format="json")

    assert root_response.status_code == 200
    assert root_response.data["play"].endswith(play_path)
    assert invalid_response.status_code == 400
    assert invalid_response.content == b"no items requested"


def test_obr_sync_api_requires_its_dedicated_permission(api_client):
    path = reverse("api:obr-sync:artist-list")

    anonymous_response = api_client.get(path)
    user = get_user_model().objects.create_user(username="obr-sync-unprivileged")
    api_client.force_authenticate(user=user)
    authenticated_response = api_client.get(path)

    assert anonymous_response.status_code == 401
    assert authenticated_response.status_code == 403
    assert authenticated_response.data["detail"] == "Insufficient permissions"


@pytest.mark.parametrize(
    "url_name",
    [
        "api:obr-sync:artist-list",
        "api:obr-sync:emission-list",
        "api:obr-sync:tag-list",
    ],
)
def test_obr_sync_representative_lists_keep_their_paginated_contract(
    api_client, obr_sync_user, url_name
):
    path = reverse(url_name)
    match = resolve(path)
    api_client.force_authenticate(user=obr_sync_user)

    assert match.url_name == url_name.split(":")[-1]
    assert_paginated_empty_response(api_client.get(path))


def test_obr_sync_artist_detail_serializes_sync_identity_fields(
    api_client, obr_sync_user
):
    artist = Artist.objects.create(name="OBR Sync Artist", d_tags="")
    path = reverse("api:obr-sync:artist-detail", kwargs={"uuid": artist.uuid})
    api_client.force_authenticate(user=obr_sync_user)

    response = api_client.get(path)

    assert response.status_code == 200
    assert response.data["uuid"] == str(artist.uuid)
    assert response.data["name"] == artist.name
    assert response.data["ct"] == "alibrary.artist"
    assert response.data["url"].endswith(path)
