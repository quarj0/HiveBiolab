import json

from django.test import Client, TestCase
from django.urls import reverse

from .models import TrainingRegistration


class TrainingAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("training_register")

    def test_register_participant_success(self):
        payload = {
            "full_name": "Bianca Lab",
            "email": "bianca@biolab.org",
            "program": "Synthetic Biology",
            "phone": "+233501234567",
        }
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        registration = TrainingRegistration.objects.get(email="bianca@biolab.org")
        self.assertEqual(response.json().get("registration_id"), registration.pk)

    def test_register_requires_fields(self):
        payload = {"full_name": "", "email": "test@biolab.org", "program": ""}
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_register_requires_valid_json(self):
        response = self.client.post(
            self.url, data="bad", content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
