from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response

class LandingPageView(TemplateView):
    template_name = "monitoring/landing.html"

class HealthView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({
            "status": "healthy"
        })