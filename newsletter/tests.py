import json

from django.test import Client, TestCase
from django.urls import reverse

from .models import NewsletterSubscriber


class NewsletterAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("newsletter_subscribe")

    def test_subscribe_success(self):
        payload = {"email": "test@biolab.org", "name": "Test User"}
        response = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        subscriber = NewsletterSubscriber.objects.get(email="test@biolab.org")
        self.assertEqual(response.json().get("subscription_id"), subscriber.pk)

    def test_subscribe_requires_valid_json(self):
        response = self.client.post(
            self.url, data="not-json", content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_subscribe_requires_email(self):
        response = self.client.post(
            self.url,
            data=json.dumps({"email": "", "name": "No Email"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
