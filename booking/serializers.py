from rest_framework import serializers
from .models import CompanyProfile

class CompanyProfileSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='name')

    class Meta:
        model = CompanyProfile
        fields = [
            'company_name',
            'brand_color',
            'logo',
            'currency',
            'contact_email',
            'contact_phone',
            'event_type_label',
            'event_label',
            'availability_free_label',
            'availability_regular_label',
            'availability_no_free_label',
            'extras_label',
        ]
