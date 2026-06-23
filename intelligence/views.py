from rest_framework.views import APIView
from rest_framework.response import Response

from .services.ingestion_service import IngestionService

from rest_framework import generics

from .models import IntelligenceRecord

from .serializers import (
    IntelligenceRecordSerializer
)


# Create your views here.

class IntelligenceListView(generics.ListAPIView):
    queryset = IntelligenceRecord.objects.all()
    serializer_class = IntelligenceRecordSerializer
    filterset_fields = ["source", "category", "severity"]

class OTXIngestView(APIView):
    def post(self, request):
        service = IngestionService()
        count = service.ingest_otx()

        return Response({
            "status": "success",
            "source": "OTX",
            "ingested_records": count
        })