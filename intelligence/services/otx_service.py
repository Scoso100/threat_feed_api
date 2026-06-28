# intelligence/services/otx_service.py

from urllib.parse import urljoin

import requests
from django.conf import settings


class OTXService:

    BASE_URL = "https://otx.alienvault.com/api/v1"
    REQUEST_TIMEOUT = (10, 60)

    def fetch_pulses(self, limit=50, max_pages=None):
        """
        Fetch subscribed OTX pulses from AlienVault OTX, following pagination.
        This class does not save data to the database.
        """
        api_key = settings.OTX_API_KEY.strip()

        if not api_key:
            raise ValueError("OTX_API_KEY is not configured.")

        headers = {
            "X-OTX-API-KEY": api_key,
            "User-Agent": "threat-feed-api/1.0",
        }

        url = f"{self.BASE_URL}/pulses/subscribed"
        params = {"limit": limit}
        pulses = []
        pages_fetched = 0

        while url:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=self.REQUEST_TIMEOUT,
            )

            response.raise_for_status()
            data = response.json()

            pulses.extend(data.get("results", []))
            pages_fetched += 1

            if max_pages and pages_fetched >= max_pages:
                break

            next_url = data.get("next")
            url = urljoin(response.url, next_url) if next_url else None
            params = None

        return {
            "results": pulses,
            "pages_fetched": pages_fetched,
            "record_count": len(pulses),
        }
