from django.urls import path
from .views import (
    IntelligenceListView,
    OTXIngestView,
)

urlpatterns = [
    path("", IntelligenceListView.as_view(), name="intelligence-list"),
    path("ingest/otx/", OTXIngestView.as_view(), name="otx-ingest"),
]