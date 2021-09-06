# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alibrary", "0007_relation_uuid"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="artist",
            options={
                "ordering": ("name",),
                "verbose_name": "Artist",
                "verbose_name_plural": "Artists",
                "permissions": (
                    ("edit_artist", "Edit Artist"),
                    ("merge_artist", "Merge Artists"),
                ),
            },
        ),
        migrations.AlterModelOptions(
            name="label",
            options={
                "ordering": ("name",),
                "verbose_name": "Label",
                "verbose_name_plural": "Labels",
                "permissions": (
                    ("edit_label", "Edit Label"),
                    ("merge_label", "Merge Labels"),
                ),
            },
        ),
        migrations.AlterModelOptions(
            name="media",
            options={
                "ordering": ("medianumber", "tracknumber", "name"),
                "verbose_name": "Track",
                "verbose_name_plural": "Tracks",
                "permissions": (
                    ("play_media", "Play Track"),
                    ("downoad_media", "Download Track"),
                    ("download_master", "Download Master"),
                    ("edit_media", "Edit Track"),
                    ("merge_media", "Merge Tracks"),
                    ("reassign_media", "Re-assign Tracks"),
                    ("admin_media", "Edit Track (extended)"),
                    ("upload_media", "Upload Track"),
                ),
            },
        ),
    ]
