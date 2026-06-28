from django.db import models

# Create your models here.

class IntelligenceRecord(models.Model):
    title = models.CharField(max_length=255)
    source = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    external_id = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    severity = models.CharField(max_length=50, default="Medium")
    author_name = models.CharField(max_length=255, blank=True)
    pulse_url = models.URLField(max_length=500, blank=True)
    tlp = models.CharField(max_length=50, blank=True)
    tags = models.JSONField(default=list, blank=True)
    references = models.JSONField(default=list, blank=True)
    indicators = models.JSONField(default=list, blank=True)
    indicator_count = models.PositiveIntegerField(default=0)
    raw_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    modified_at = models.DateTimeField(null=True, blank=True)
    ingested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
