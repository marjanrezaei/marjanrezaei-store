from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class ContactAPIEnglishTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('website_api:contact_api')
        self.valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "+971501234567",
            "details": "Hello, I have a question about your service."
        }

    def test_successful_submission(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Your message was sent successfully!")

    def test_missing_email_field(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop("email")
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)