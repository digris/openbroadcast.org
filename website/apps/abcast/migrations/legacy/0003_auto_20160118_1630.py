# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abcast', '0002_auto_20160114_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='daypart',
            name='enable_autopilot',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='weekday',
            name='day',
            field=models.PositiveIntegerField(default=0, choices=[(6, 'Sun'), (0, 'Mon'), (1, 'Tue'), (2, 'Wed'), (3, 'Thu'), (4, 'Fri'), (5, 'Sat')]),
        ),
    ]
