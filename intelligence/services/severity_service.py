import re


class SeverityService:
    CRITICAL_TERMS = (
        "active exploitation",
        "critical vulnerability",
        "destructive",
        "exploited in the wild",
        "ransomware",
        "supply chain",
        "wiper",
        "zero-day",
        "0-day",
    )
    HIGH_TERMS = (
        "apt",
        "backdoor",
        "botnet",
        "c2",
        "command-and-control",
        "credential",
        "exploit",
        "infostealer",
        "loader",
        "malware",
        "phishing",
        "rat",
        "remote access",
        "stealer",
        "trojan",
    )

    def score_pulse(self, pulse, indicators=None):
        indicators = indicators or pulse.get("indicators") or []
        indicator_count = len(indicators)
        text = self._searchable_text(pulse)
        tlp = str(pulse.get("TLP") or pulse.get("tlp") or "").lower()

        if tlp == "red":
            return "Critical"

        if self._contains_any(text, self.CRITICAL_TERMS):
            if indicator_count >= 50 or self._has_cve(text):
                return "Critical"
            return "High"

        if indicator_count >= 500:
            return "Critical"

        if tlp in ("amber", "amber+strict"):
            return "High"

        if indicator_count >= 100:
            return "High"

        if self._contains_any(text, self.HIGH_TERMS):
            return "High"

        if indicator_count >= 10 or pulse.get("references") or pulse.get("tags"):
            return "Medium"

        return "Low"

    def score_record(self, record):
        pulse = record.raw_data or {
            "name": record.title,
            "description": record.description,
            "tags": record.tags,
            "references": record.references,
            "tlp": record.tlp,
            "indicators": record.indicators,
        }

        return self.score_pulse(pulse, record.indicators)

    def _contains_any(self, text, terms):
        return any(term in text for term in terms)

    def _has_cve(self, text):
        return bool(re.search(r"\bcve-\d{4}-\d{4,7}\b", text))

    def _searchable_text(self, pulse):
        parts = [
            pulse.get("name", ""),
            pulse.get("description", ""),
            pulse.get("adversary", ""),
        ]
        parts.extend(pulse.get("tags") or [])
        parts.extend(pulse.get("malware_families") or [])
        parts.extend(pulse.get("attack_ids") or [])

        return " ".join(str(part).lower() for part in parts if part)
