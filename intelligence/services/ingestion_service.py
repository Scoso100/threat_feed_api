# intelligence/services/ingestion_service.py

from datetime import timezone as datetime_timezone

from django.utils import timezone
from django.utils.dateparse import parse_datetime

from intelligence.models import IntelligenceRecord
from .otx_service import OTXService
from .severity_service import SeverityService


class IngestionService:

    def ingest_otx(self, limit=50, max_pages=None):

        service = OTXService()
        severity_service = SeverityService()
        data = service.fetch_pulses(limit=limit, max_pages=max_pages)
        created_count = 0
        updated_count = 0

        for pulse in data.get("results", []):
            indicators = pulse.get("indicators") or []

            _, created = IntelligenceRecord.objects.update_or_create(
                external_id=pulse["id"],
                defaults={
                    "title": pulse.get("name", ""),
                    "source": "OTX",
                    "category": "THREAT",
                    "description": pulse.get("description", ""),
                    "severity": severity_service.score_pulse(pulse, indicators),
                    "author_name": pulse.get("author_name", ""),
                    "pulse_url": self._pulse_url(pulse),
                    "tlp": pulse.get("TLP") or pulse.get("tlp") or "",
                    "tags": pulse.get("tags") or [],
                    "references": pulse.get("references") or [],
                    "indicators": indicators,
                    "indicator_count": len(indicators),
                    "raw_data": pulse,
                    "created_at": self._parse_otx_datetime(pulse.get("created")),
                    "modified_at": self._parse_otx_datetime(pulse.get("modified")),
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        return {
            "processed": len(data.get("results", [])),
            "created": created_count,
            "updated": updated_count,
            "pages_fetched": data.get("pages_fetched", 0),
        }

    def _pulse_url(self, pulse):
        pulse_id = pulse.get("id")

        if not pulse_id:
            return ""

        return f"https://otx.alienvault.com/pulse/{pulse_id}"

    def _parse_otx_datetime(self, value):
        if not value:
            return None

        parsed = parse_datetime(value)

        if parsed and timezone.is_naive(parsed):
            return parsed.replace(tzinfo=datetime_timezone.utc)

        return parsed
