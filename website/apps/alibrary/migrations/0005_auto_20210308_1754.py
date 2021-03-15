# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("alibrary", "0004_auto_20200515_1931"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="label",
            name="founding_artist",
        ),
        migrations.AlterField(
            model_name="relation",
            name="service",
            field=models.CharField(
                default="generic",
                choices=[
                    ("", "Not specified"),
                    ("generic", "Generic"),
                    ("facebook", "Facebook"),
                    ("youtube", "YouTube"),
                    ("discogs", "Discogs"),
                    ("lastfm", "Last.fm"),
                    ("linkedin", "Linked In"),
                    ("soundcloud", "Soundcloud"),
                    ("twitter", "Twitter"),
                    ("discogs_master", "Discogs | master-release"),
                    ("wikipedia", "Wikipedia"),
                    ("musicbrainz", "Musicbrainz"),
                    ("bandcamp", "Bandcamp"),
                    ("itunes", "iTunes"),
                    ("imdb", "IMDb"),
                    ("wikidata", "wikidata"),
                    ("viaf", "VIAF"),
                    ("official", "Official website"),
                    ("vimeo", "Vimeo"),
                    ("instagram", "Instagram"),
                    ("ndr", "NDR"),
                ],
                max_length=50,
                blank=True,
                null=True,
                db_index=True,
            ),
        ),
        migrations.AlterField(
            model_name="release",
            name="label",
            field=models.ForeignKey(
                related_name="releases",
                on_delete=django.db.models.deletion.SET_NULL,
                blank=True,
                to="alibrary.Label",
                null=True,
            ),
        ),
    ]
