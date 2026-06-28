from collections import Counter

from django.db.models import Count, Sum
from requests import RequestException
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .services.ingestion_service import IngestionService

from .models import IntelligenceRecord

from .serializers import (
    IntelligenceRecordListSerializer,
    IntelligenceRecordSerializer
)


# Create your views here.

class IntelligenceListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = IntelligenceRecord.objects.order_by(
        "-modified_at",
        "-created_at",
        "-ingested_at",
    )
    serializer_class = IntelligenceRecordListSerializer
    filterset_fields = ["source", "category", "severity"]


class IntelligenceDetailView(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = IntelligenceRecord.objects.all()
    serializer_class = IntelligenceRecordSerializer


class IntelligenceSummaryView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        records = IntelligenceRecord.objects.all()
        latest_records = records.order_by(
            "-modified_at",
            "-created_at",
            "-ingested_at",
        )[:10]

        return Response({
            "total_records": records.count(),
            "total_indicators": records.aggregate(
                total=Sum("indicator_count")
            )["total"] or 0,
            "by_source": self._counts(records, "source"),
            "by_category": self._counts(records, "category"),
            "by_severity": self._counts(records, "severity"),
            "top_tags": self._top_tags(records),
            "latest_records": IntelligenceRecordListSerializer(
                latest_records,
                many=True,
            ).data,
        })

    def _counts(self, queryset, field_name):
        return list(
            queryset.values(field_name)
            .annotate(count=Count("id"))
            .order_by("-count", field_name)
        )

    def _top_tags(self, queryset, limit=10):
        counter = Counter()

        for tags in queryset.values_list("tags", flat=True):
            counter.update(tags or [])

        return [
            {"tag": tag, "count": count}
            for tag, count in counter.most_common(limit)
        ]


class OTXIngestView(APIView):
    def post(self, request):
        limit = self._positive_int(request, "limit", 50)
        max_pages = self._positive_int(request, "max_pages", None)

        if limit is None:
            return Response(
                {"detail": "limit must be a positive integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if max_pages is None and self._has_value(request, "max_pages"):
            return Response(
                {"detail": "max_pages must be a positive integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service = IngestionService()

        try:
            result = service.ingest_otx(limit=limit, max_pages=max_pages)
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except RequestException as exc:
            return Response(
                {
                    "detail": "OTX request failed.",
                    "error": str(exc),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response({
            "status": "success",
            "source": "OTX",
            "ingested_records": result["processed"],
            "created": result["created"],
            "updated": result["updated"],
            "pages_fetched": result["pages_fetched"],
        })

    def _positive_int(self, request, name, default):
        value = request.data.get(name, request.query_params.get(name, default))

        if value in ("", None):
            return default

        try:
            parsed = int(value)
        except (TypeError, ValueError):
            return None

        if parsed < 1:
            return None

        return parsed

    def _has_value(self, request, name):
        return name in request.data or name in request.query_params
