from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import time
from .models import CompanyProfile, CompanyWeekdaySlot

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


class BusinessHoursAPITest(APITestCase):
    def setUp(self):
        self.profile = CompanyProfile.get_solo()
        self.url = reverse('api-business-hours')
        
        # Create some test slots
        CompanyWeekdaySlot.objects.create(
            company=self.profile,
            weekday=0, # Monday
            start_time=time(9, 0),
            end_time=time(17, 0)
        )
        CompanyWeekdaySlot.objects.create(
            company=self.profile,
            weekday=1, # Tuesday
            start_time=time(10, 0),
            end_time=time(14, 0)
        )

    def test_get_business_hours_success(self):
        """
        Verify that GET /api/business-hours/ returns 200 and the correct JSON structure.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(len(data), 2)
        
        # Verify ordering and content
        self.assertEqual(data[0]['weekday'], 0)
        self.assertEqual(data[0]['start_time'], "09:00:00")
        self.assertEqual(data[0]['end_time'], "17:00:00")

        self.assertEqual(data[1]['weekday'], 1)
        self.assertEqual(data[1]['start_time'], "10:00:00")
        self.assertEqual(data[1]['end_time'], "14:00:00")

    def test_public_access(self):
        """
        Verify that the business hours endpoint is accessible without authentication.
        """
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
