from rest_framework import serializers

from .models import IntelligenceRecord


class IntelligenceRecordSerializer(
    serializers.ModelSerializer
):
    
    class Meta:
        model = IntelligenceRecord
        fields = "__all__"