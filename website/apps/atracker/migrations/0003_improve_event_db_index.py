from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atracker', '0002_added_object_pk_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation date', db_index=True),
        ),
    ]
