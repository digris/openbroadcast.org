# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0029_auto_20170508_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='mixdown_file',
            field=models.FileField(null=True, upload_to=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='release',
            name='releasetype',
            field=models.CharField(blank=True, max_length=24, null=True, verbose_name='Release type', choices=[('General', ((b'album', 'Album'), (b'single', 'Single'), (b'ep', 'EP'), (b'compilation', 'Compilation'), (b'soundtrack', 'Soundtrack'), (b'audiobook', 'Audiobook'), (b'spokenword', 'Spokenword'), (b'interview', 'Interview'), (b'jingle', 'Jingle'), (b'live', 'Live'), (b'remix', 'Remix'), (b'broadcast', 'Broadcast'), (b'djmix', 'DJ-Mix'), (b'mixtape', 'Mixtape'))), (b'other', 'Other')]),
        ),
    ]
