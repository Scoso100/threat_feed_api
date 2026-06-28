from django.urls import path
from .views import (
    IntelligenceDetailView,
    IntelligenceListView,
    IntelligenceSummaryView,
    OTXIngestView,
)

urlpatterns = [
    path("", IntelligenceListView.as_view(), name="intelligence-list"),
    path("summary/", IntelligenceSummaryView.as_view(), name="intelligence-summary"),
    path("<int:pk>/", IntelligenceDetailView.as_view(), name="intelligence-detail"),
    path("ingest/otx/", OTXIngestView.as_view(), name="otx-ingest"),
]
