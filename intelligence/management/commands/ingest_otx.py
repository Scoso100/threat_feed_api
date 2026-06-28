from django.core.management.base import BaseCommand, CommandError
from requests import RequestException

from intelligence.services.ingestion_service import IngestionService


class Command(BaseCommand):
    help = "Ingest subscribed AlienVault OTX pulses."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=50,
            help="Number of OTX pulses to request per page.",
        )
        parser.add_argument(
            "--max-pages",
            type=int,
            default=None,
            help="Maximum number of OTX pages to fetch.",
        )

    def handle(self, *args, **options):
        limit = options["limit"]
        max_pages = options["max_pages"]

        if limit < 1:
            self.stderr.write("limit must be a positive integer.")
            return

        if max_pages is not None and max_pages < 1:
            self.stderr.write("max-pages must be a positive integer.")
            return

        try:
            result = IngestionService().ingest_otx(
                limit=limit,
                max_pages=max_pages,
            )
        except ValueError as exc:
            raise CommandError(str(exc)) from exc
        except RequestException as exc:
            raise CommandError(f"OTX request failed: {exc}") from exc

        self.stdout.write(
            self.style.SUCCESS(
                "Processed {processed} OTX pulses "
                "({created} created, {updated} updated) "
                "across {pages_fetched} page(s).".format(**result)
            )
        )
