# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20160526_1618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='community',
            name='description_html',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='biography_html',
        ),
        migrations.AlterField(
            model_name='profile',
            name='pseudonym',
            field=models.CharField(help_text='Will appear instead of your first- & last name', max_length=250, null=True, blank=True),
        ),
    ]
