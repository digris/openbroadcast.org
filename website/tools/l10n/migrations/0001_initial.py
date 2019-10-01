# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AdminArea",
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
                    "name",
                    models.CharField(max_length=60, verbose_name="Admin Area name"),
                ),
                (
                    "abbrev",
                    models.CharField(
                        max_length=3,
                        null=True,
                        verbose_name="Postal Abbreviation",
                        blank=True,
                    ),
                ),
                (
                    "active",
                    models.BooleanField(default=True, verbose_name="Area is active"),
                ),
            ],
            options={
                "ordering": ("name",),
                "verbose_name": "Administrative Area",
                "verbose_name_plural": "Administrative Areas",
            },
        ),
        migrations.CreateModel(
            name="Country",
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
                    "iso2_code",
                    models.CharField(
                        unique=True, max_length=2, verbose_name="ISO alpha-2"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=128, verbose_name="Official name (CAPS)"
                    ),
                ),
                (
                    "printable_name",
                    models.CharField(max_length=128, verbose_name="Country name"),
                ),
                (
                    "iso3_code",
                    models.CharField(
                        unique=True, max_length=3, verbose_name="ISO alpha-3"
                    ),
                ),
                (
                    "numcode",
                    models.PositiveSmallIntegerField(
                        null=True, verbose_name="ISO numeric", blank=True
                    ),
                ),
                (
                    "active",
                    models.BooleanField(default=True, verbose_name="Country is active"),
                ),
                (
                    "continent",
                    models.CharField(
                        max_length=2,
                        verbose_name="Continent",
                        choices=[
                            (b"AF", "Africa"),
                            (b"NA", "North America"),
                            (b"EU", "Europe"),
                            (b"AS", "Asia"),
                            (b"OC", "Oceania"),
                            (b"SA", "South America"),
                            (b"AN", "Antarctica"),
                            (b"WX", "Worldwide"),
                        ],
                    ),
                ),
                (
                    "admin_area",
                    models.CharField(
                        blank=True,
                        max_length=2,
                        null=True,
                        verbose_name="Administrative Area",
                        choices=[
                            (b"a", "Another"),
                            (b"i", "Island"),
                            (b"ar", "Arrondissement"),
                            (b"at", "Atoll"),
                            (b"ai", "Autonomous island"),
                            (b"ca", "Canton"),
                            (b"cm", "Commune"),
                            (b"co", "County"),
                            (b"dp", "Department"),
                            (b"de", "Dependency"),
                            (b"dt", "District"),
                            (b"dv", "Division"),
                            (b"em", "Emirate"),
                            (b"gv", "Governorate"),
                            (b"ic", "Island council"),
                            (b"ig", "Island group"),
                            (b"ir", "Island region"),
                            (b"kd", "Kingdom"),
                            (b"mu", "Municipality"),
                            (b"pa", "Parish"),
                            (b"pf", "Prefecture"),
                            (b"pr", "Province"),
                            (b"rg", "Region"),
                            (b"rp", "Republic"),
                            (b"sh", "Sheading"),
                            (b"st", "State"),
                            (b"sd", "Subdivision"),
                            (b"sj", "Subject"),
                            (b"ty", "Territory"),
                        ],
                    ),
                ),
            ],
            options={
                "ordering": ("printable_name",),
                "verbose_name": "Country",
                "verbose_name_plural": "Countries",
            },
        ),
        migrations.AddField(
            model_name="adminarea",
            name="country",
            field=models.ForeignKey(to="l10n.Country"),
        ),
    ]
