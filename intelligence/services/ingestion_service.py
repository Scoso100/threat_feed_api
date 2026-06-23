# intelligence/services/ingestion_service.py

from intelligence.models import IntelligenceRecord
from .otx_service import OTXService



class IngestionService:

    def ingest_otx(self):

        service = OTXService()
        data = service.fetch_pulses()

        for pulse in data.get("results", []):

            IntelligenceRecord.objects.update_or_create(
                external_id=pulse["id"],
                defaults={
                    "title": pulse["name"],
                    "source": "OTX",
                    "category": "THREAT",
                    "description": pulse.get("description", ""),
                    "severity": "Medium",
                    "created_at": pulse.get("modified")
                }
            )

        return len(data.get("results", []))

    
