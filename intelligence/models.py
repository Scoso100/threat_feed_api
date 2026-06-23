from django.db import models

# Create your models here.

class IntelligenceRecord(models.Model):
    title = models.CharField(max_length=255)
    source = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    external_id = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    severity = models.CharField(max_length=50, default="Medium")
    created_at = models.DateTimeField(null=True, blank=True)
    ingested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title