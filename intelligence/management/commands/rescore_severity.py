from collections import Counter

from django.core.management.base import BaseCommand

from intelligence.models import IntelligenceRecord
from intelligence.services.severity_service import SeverityService


class Command(BaseCommand):
    help = "Recalculate severity for existing intelligence records."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Calculate severity distribution without saving changes.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        severity_service = SeverityService()
        counts = Counter()
        updated = 0

        for record in IntelligenceRecord.objects.all().iterator():
            severity = severity_service.score_record(record)
            counts[severity] += 1

            if record.severity == severity:
                continue

            if dry_run:
                updated += 1
                continue

            record.severity = severity
            record.save(update_fields=["severity"])
            updated += 1

        prefix = "Would update" if dry_run else "Updated"
        distribution = ", ".join(
            f"{severity}: {count}"
            for severity, count in sorted(counts.items())
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"{prefix} {updated} record(s). Distribution: {distribution}"
            )
        )
