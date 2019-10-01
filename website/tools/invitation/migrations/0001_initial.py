# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Invitation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("email", models.EmailField(max_length=254, verbose_name="e-mail")),
                ("message", models.TextField(null=True)),
                (
                    "key",
                    models.CharField(
                        unique=True, max_length=40, verbose_name="invitation key"
                    ),
                ),
                (
                    "date_invited",
                    models.DateTimeField(
                        default=datetime.datetime.now, verbose_name="date invited"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        related_name="invitations", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "ordering": ("-date_invited",),
                "verbose_name": "invitation",
                "verbose_name_plural": "invitations",
            },
        ),
        migrations.CreateModel(
            name="InvitationStats",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "available",
                    models.IntegerField(
                        default=5, verbose_name="available invitations"
                    ),
                ),
                (
                    "sent",
                    models.IntegerField(default=0, verbose_name="invitations sent"),
                ),
                (
                    "accepted",
                    models.IntegerField(default=0, verbose_name="invitations accepted"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        related_name="invitation_stats", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "ordering": ("-user",),
                "verbose_name": "invitation stats",
                "verbose_name_plural": "invitation stats",
            },
        ),
    ]
