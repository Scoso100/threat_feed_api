# intelligence/services/otx_service.py

import requests
from django.conf import settings


class OTXService:

    BASE_URL = "https://otx.alienvault.com/api/v1"

    def fetch_pulses(self):
        """
        Fetch subscribed OTX pulses from AlienVault OTX.
        This class does not save data to the database.
        """
        headers = {
            "X-OTX-API-KEY": settings.OTX_API_KEY
        }

        response = requests.get(
            f"{self.BASE_URL}/pulses/subscribed",
            headers=headers,
            timeout=30
        )

        response.raise_for_status()
        return response.json()