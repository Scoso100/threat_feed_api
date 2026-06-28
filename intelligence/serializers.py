from rest_framework import serializers

from .models import IntelligenceRecord


class IntelligenceRecordSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = IntelligenceRecord
        fields = "__all__"


class IntelligenceRecordListSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = IntelligenceRecord
        fields = (
            "id",
            "title",
            "source",
            "category",
            "external_id",
            "description",
            "severity",
            "author_name",
            "pulse_url",
            "tlp",
            "tags",
            "references",
            "indicator_count",
            "created_at",
            "modified_at",
            "ingested_at",
        )
