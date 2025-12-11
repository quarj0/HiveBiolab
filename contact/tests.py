import json

from django.test import Client, SimpleTestCase
from django.urls import reverse
from unittest.mock import MagicMock, patch


class ContactAPITests(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("contact_submit")

    def _configure_firestore(self, mock_get_client):
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_doc = MagicMock(id="msg-123")
        mock_collection.add.return_value = (mock_doc, None)
        mock_client.collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        return mock_client, mock_doc

    def test_submit_message_success(self):
        with patch("contact.views.get_firestore_client") as mock_get_client, patch(
            "contact.views.get_server_timestamp", return_value="ts"
        ):
            mock_client, mock_doc = self._configure_firestore(mock_get_client)
            payload = {
                "name": "Ada Bio",
                "email": "ada@biolab.org",
                "subject": "Collab",
                "message": "Would love to partner on training.",
            }
            response = self.client.post(
                self.url, data=json.dumps(payload), content_type="application/json"
            )

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json().get("message_id"), mock_doc.id)
            mock_client.collection.assert_called_with("contact_messages")

    def test_submit_requires_message(self):
        payload = {"name": "No Msg", "email": "no@biolab.org", "message": ""}
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_submit_requires_valid_json(self):
        response = self.client.post(
            self.url, data="nonsense", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
