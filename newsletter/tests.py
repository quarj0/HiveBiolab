import json

from django.test import Client, SimpleTestCase
from django.urls import reverse
from unittest.mock import MagicMock, patch


class NewsletterAPITests(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("newsletter_subscribe")

    def _configure_firestore(self, mock_get_client):
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_doc = MagicMock(id="doc-uuid-123")
        mock_collection.add.return_value = (mock_doc, None)
        mock_client.collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        return mock_client, mock_doc

    def test_subscribe_success(self):
        with patch("newsletter.views.get_firestore_client") as mock_get_client, patch(
            "newsletter.views.get_server_timestamp", return_value="ts"
        ):
            mock_client, mock_doc = self._configure_firestore(mock_get_client)
            response = self.client.post(
                self.url,
                data=json.dumps({"email": "test@biolab.org", "name": "Test User"}),
                content_type="application/json",
            )

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json().get("subscription_id"), mock_doc.id)
            mock_client.collection.assert_called_with("newsletter_subscribers")

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
