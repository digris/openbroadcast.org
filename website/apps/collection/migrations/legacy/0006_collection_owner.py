# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collection', '0005_collectionmember_added_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='owner',
            field=models.ForeignKey(related_name='owned_collections', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
