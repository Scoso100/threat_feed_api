# Generated manually for OTX pulse detail storage.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("intelligence", "0002_alter_intelligencerecord_created_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="intelligencerecord",
            name="author_name",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="intelligencerecord",
            name="pulse_url",
            field=models.URLField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name="intelligencerecord",
            name="tlp",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="intelligencerecord",
            name="tags",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="intelligencerecord",
            name="references",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="intelligencerecord",
            name="indicators",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="intelligencerecord",
            name="indicator_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="intelligencerecord",
            name="raw_data",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name="intelligencerecord",
            name="modified_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
