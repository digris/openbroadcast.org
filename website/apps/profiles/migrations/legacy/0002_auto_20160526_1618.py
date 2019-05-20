# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pseudonym',
            field=models.CharField(help_text='Will appear instead of your name & surname', max_length=250, null=True, blank=True),
        ),
    ]
