from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("atracker", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="object_id",
            field=models.PositiveIntegerField(db_index=True, null=True, blank=True),
        )
    ]
