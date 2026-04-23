from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from .models import CompanyProfile
from .serializers import CompanyProfileSerializer

class CompanyConfigView(APIView):
    """
    Public endpoint to fetch company branding, contact details, and UI labels.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        config = CompanyProfile.get_solo()
        serializer = CompanyProfileSerializer(config, context={'request': request})
        data = serializer.data
        
        # Inject system timezone
        data['timezone'] = settings.TIME_ZONE
        
        return Response(data)
