# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0027_auto_20160606_1449'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='licensetranslation',
            options={'managed': True},
        ),
        migrations.RemoveField(
            model_name='agency',
            name='description_html',
        ),
        migrations.RemoveField(
            model_name='distributor',
            name='description_html',
        ),
        migrations.RemoveField(
            model_name='label',
            name='description_html',
        ),
        migrations.RemoveField(
            model_name='playlist',
            name='description_html',
        ),
        migrations.RemoveField(
            model_name='release',
            name='description_html',
        ),
        migrations.RemoveField(
            model_name='series',
            name='description_html',
        ),
        migrations.AddField(
            model_name='playlist',
            name='rotation_date_end',
            field=models.DateField(null=True, verbose_name='Rotate until', blank=True),
        ),
        migrations.AddField(
            model_name='playlist',
            name='rotation_date_start',
            field=models.DateField(null=True, verbose_name='Rotate from', blank=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='mediatype',
            field=models.CharField(default='song', max_length=128, verbose_name='Type', choices=[('Single content recording', (('song', 'Song'), ('acappella', 'A cappella'), ('soundeffects', 'Sound effects'), ('soundtrack', 'Soundtrack'), ('spokenword', 'Spokenword'), ('interview', 'Interview'), ('jingle', 'Jingle'))), ('Multiple content recording', (('djmix', 'DJ-Mix'), ('concert', 'Concert'), ('liveact', 'Live Act (PA)'), ('radioshow', 'Radio show'))), ('other', 'Other'), (None, 'Unknown')]),
        ),
    ]
