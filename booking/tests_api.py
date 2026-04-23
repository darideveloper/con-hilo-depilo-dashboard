from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import CompanyProfile

class ConfigAPITest(APITestCase):
    def setUp(self):
        self.profile = CompanyProfile.get_solo()
        self.profile.name = "Test Company"
        self.profile.brand_color = "#ee5837"
        self.profile.event_type_label = "Special Category"
        self.profile.save()
        self.url = reverse('api-config')

    def test_get_config_success(self):
        """
        Verify that GET /api/config/ returns 200 and the correct JSON structure.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(data['company_name'], "Test Company")
        self.assertEqual(data['brand_color'], "#ee5837")
        self.assertEqual(data['event_type_label'], "Special Category")
        self.assertIn('timezone', data)
        self.assertIn('currency', data)
        self.assertIn('logo', data)

    def test_public_access(self):
        """
        Verify that the endpoint is accessible without authentication.
        """
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
