import uuid
from types import SimpleNamespace

from wand.image import Image

from metadata_generator.dab import generator


def test_compose_main_slide_writes_valid_jpeg(monkeypatch, tmp_path):
    emission_uuid = uuid.uuid4()
    media_uuid = uuid.uuid4()
    monkeypatch.setattr(generator, "SLIDE_BASE_DIR", str(tmp_path))
    monkeypatch.setattr(generator, "IMAGE_OUTPUT_FORMAT", "jpg")

    dab_generator = generator.DABMetadataGenerator(
        emission=SimpleNamespace(uuid=emission_uuid, content_object=None),
        content_object=SimpleNamespace(uuid=media_uuid),
    )

    url = dab_generator.compose_main_slide(
        primary_text="A Short Track",
        secondary_text="by Example Artist",
        overlay_image_path=generator.SLIDE_DEFAULT_IMAGE,
    )

    expected_filename = f"{emission_uuid}-{media_uuid}-000.jpg"
    output_path = tmp_path / expected_filename
    debug_path = tmp_path / "debug-0.jpg"

    assert url == f"{generator.SLIDE_BASE_URL}{expected_filename}"
    assert output_path.exists()
    assert debug_path.exists()

    with Image(filename=str(output_path)) as image:
        assert image.format == "JPEG"
        assert image.size == (320, 240)
