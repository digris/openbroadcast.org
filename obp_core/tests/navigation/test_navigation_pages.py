from types import SimpleNamespace
from uuid import uuid4

import pytest
from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve, reverse
from elasticsearch_dsl import FacetedSearch

from abcast.models import Channel
from alibrary.models import Playlist


pytestmark = pytest.mark.django_db


class EmptySearchResult:
    """Small Elasticsearch stand-in for rendering otherwise live list pages."""

    hits = SimpleNamespace(total=0)

    class EmptyFacets:
        def __getattr__(self, name):
            return []

    facets = EmptyFacets()

    def to_dict(self):
        return {
            "hits": {
                "hits": [],
                "total": 0,
                "max_score": None,
            }
        }


@pytest.fixture(autouse=True)
def empty_search_results(monkeypatch):
    """Keep navigation tests independent of the external Elasticsearch service."""

    monkeypatch.setattr(FacetedSearch, "execute", lambda self: EmptySearchResult())


@pytest.fixture
def admin_user():
    return get_user_model().objects.create_superuser(
        username="navigation-admin",
        email="navigation@example.com",
        password="test-password",
    )


def assert_page(client, url_name, expected_menu_item, *, kwargs=None):
    url = reverse(url_name, kwargs=kwargs)
    match = resolve(url)

    assert match.func.view_class

    response = client.get(url)

    assert response.status_code == 200
    assert response.resolver_match.url_name == match.url_name
    assert response.context["current_menu_item"] == expected_menu_item

    return response


@pytest.mark.parametrize(
    ("url_name", "menu_item"),
    [
        ("alibrary:release-list", "catalog:release-list"),
        ("alibrary:artist-list", "catalog:artist-list"),
        ("alibrary:media-list", "catalog:media-list"),
        ("alibrary:label-list", "catalog:label-list"),
    ],
)
def test_catalog_list_pages_render_with_their_navigation_section(
    client, url_name, menu_item
):
    assert_page(client, url_name, menu_item)


@pytest.mark.parametrize(
    ("url_names", "menu_item"),
    [
        (
            (
                "alibrary:release-list",
                "alibrary:release-detail",
                "alibrary:release-edit",
            ),
            "catalog:release-list",
        ),
        (
            (
                "alibrary:artist-list",
                "alibrary:artist-detail",
                "alibrary:artist-edit",
            ),
            "catalog:artist-list",
        ),
        (
            (
                "alibrary:media-list",
                "alibrary:media-detail",
                "alibrary:media-edit",
            ),
            "catalog:media-list",
        ),
        (
            (
                "alibrary:label-list",
                "alibrary:label-detail",
                "alibrary:label-edit",
            ),
            "catalog:label-list",
        ),
    ],
)
def test_catalog_related_routes_keep_the_same_navigation_section(url_names, menu_item):
    list_name, detail_name, edit_name = url_names
    routes = (
        reverse(list_name),
        reverse(detail_name, kwargs={"uuid": uuid4()}),
        reverse(edit_name, kwargs={"pk": 1}),
    )

    for route in routes:
        view_class = resolve(route).func.view_class
        assert view_class.current_menu_item == menu_item


@pytest.mark.parametrize(
    ("url_name", "menu_item"),
    [
        ("alibrary:playlist-list", "catalog-playlists:playlist-list"),
        ("alibrary:playlist-list-own", "catalog-playlists:playlist-list-own"),
    ],
)
def test_playlist_list_pages_render_with_public_or_own_navigation(
    client, admin_user, url_name, menu_item
):
    client.force_login(admin_user)
    assert_page(client, url_name, menu_item)


def test_playlist_detail_navigation_depends_on_ownership(client, admin_user):
    other_user = get_user_model().objects.create_user(username="playlist-owner")
    own_playlist = Playlist.objects.create(
        name="Own playlist",
        type=Playlist.TYPE_PLAYLIST,
        user=admin_user,
    )
    public_playlist = Playlist.objects.create(
        name="Public playlist",
        type=Playlist.TYPE_PLAYLIST,
        user=other_user,
    )
    client.force_login(admin_user)

    assert_page(
        client,
        "alibrary:playlist-detail",
        "catalog-playlists:playlist-list-own",
        kwargs={"uuid": own_playlist.uuid},
    )
    assert_page(
        client,
        "alibrary:playlist-detail",
        "catalog-playlists:playlist-list",
        kwargs={"uuid": public_playlist.uuid},
    )


def test_playlist_create_edit_and_delete_use_own_navigation(client, admin_user):
    playlist = Playlist.objects.create(
        name="Editable playlist",
        type=Playlist.TYPE_BASKET,
        user=admin_user,
        d_tags="",
    )
    client.force_login(admin_user)
    own_menu_item = "catalog-playlists:playlist-list-own"

    create_view = resolve(reverse("alibrary:playlist-create")).func.view_class
    assert create_view.current_menu_item == own_menu_item
    assert_page(
        client,
        "alibrary:playlist-edit",
        own_menu_item,
        kwargs={"uuid": playlist.uuid},
    )
    assert_page(
        client,
        "alibrary:playlist-delete",
        own_menu_item,
        kwargs={"pk": playlist.pk},
    )


def test_importer_page_renders_under_data_navigation(client, admin_user):
    client.force_login(admin_user)
    assert_page(client, "importer:import-list", "data:importer")


def test_exporter_page_renders_under_data_navigation(client):
    assert_page(client, "exporter:export-index", "data:exporter")


@pytest.mark.parametrize(
    ("url_name", "menu_item"),
    [
        ("profiles:profile-list", "network:profile-list"),
        ("abcast-network:station-list", "network:station-list"),
        ("actstream:action-list", "network:activity-list"),
    ],
)
def test_network_list_pages_render_with_their_navigation_section(
    client, url_name, menu_item
):
    assert_page(client, url_name, menu_item)


def test_scheduler_page_renders_under_scheduler_navigation(client):
    Channel.objects.create(pk=1, name="Test channel", has_scheduler=True)
    assert_page(client, "abcast:scheduler", "scheduler")
