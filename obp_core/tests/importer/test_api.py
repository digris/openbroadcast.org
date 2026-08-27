import uuid
from datetime import datetime
from types import SimpleNamespace

from importer.api import ImportFileResource


def test_import_file_media_field_stays_shallow_for_list_and_detail():
    resource = ImportFileResource()
    media_field = resource.fields["media"]

    assert media_field.full is False
    assert media_field.full_list(None) is False
    assert media_field.full_detail(None) is False


def test_import_file_media_payload_is_compact_and_non_recursive():
    resource = ImportFileResource()
    artist = SimpleNamespace(
        pk=2,
        uuid=uuid.uuid4(),
        name="Artist",
        get_absolute_url=lambda: "/artist/",
    )
    release_image = SimpleNamespace(url="/media/release.jpg")
    release = SimpleNamespace(
        pk=3,
        uuid=uuid.uuid4(),
        name="Release",
        main_image=release_image,
        get_absolute_url=lambda: "/release/",
    )
    media = SimpleNamespace(
        pk=1,
        uuid=uuid.uuid4(),
        name="Track",
        created=datetime(2026, 8, 27, 12, 0, 0),
        artist=artist,
        release=release,
        get_absolute_url=lambda: "/track/",
        get_api_url=lambda: "/api/v1/library/track/1/",
    )

    data = resource._dehydrate_media(media)

    assert data["id"] == media.pk
    assert data["uuid"] == str(media.uuid)
    assert data["name"] == "Track"
    assert data["absolute_url"] == "/track/"
    assert data["resource_uri"] == "/api/v1/library/track/1/"
    assert data["artist"]["name"] == "Artist"
    assert data["artist"]["absolute_url"] == "/artist/"
    assert data["release"]["name"] == "Release"
    assert data["release"]["main_image"] == "/media/release.jpg"
    assert "media" not in data["release"]
