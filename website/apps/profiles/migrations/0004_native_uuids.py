# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


def concat_uuids(apps, schema_editor):

    items = [
        'Profile',
        'Community',
    ]

    for item in items:
        qs = apps.get_model("profiles", item)
        for obj in qs.objects.using(schema_editor.connection.alias).all():
            qs.objects.filter(pk=obj.pk).update(uuid=obj.uuid.replace('-', ''))



def forwards(apps, schema_editor):
    if not schema_editor.connection.vendor == 'postgresql':
        print('db backend not postgres - skipping table update')
        return
    migrations.RunSQL("""
alter table user_profiles alter column uuid type uuid using uuid::uuid;
alter table profiles_community alter column uuid type uuid using uuid::uuid;
""")



class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20170725_1409'),
    ]

    operations = [

        migrations.RunPython(concat_uuids),

        migrations.RunPython(forwards, None, [
            migrations.AlterField(
                model_name='community',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False, db_index=True),
            ),
            migrations.AlterField(
                model_name='profile',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False, db_index=True),
            ),
        ]),
    ]
