from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("importer", "0001_initial"),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name="importitem",
            index_together={("content_type", "object_id")},
        ),
    ]
