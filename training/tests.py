import json

from django.test import Client, SimpleTestCase
from django.urls import reverse
from unittest.mock import MagicMock, patch


class TrainingAPITests(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("training_register")

    def _configure_firestore(self, mock_get_client):
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_doc = MagicMock(id="reg-123")
        mock_collection.add.return_value = (mock_doc, None)
        mock_client.collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        return mock_client, mock_doc

    def test_register_participant_success(self):
        with patch("training.views.get_firestore_client") as mock_get_client, patch(
            "training.views.get_server_timestamp", return_value="ts"
        ):
            mock_client, mock_doc = self._configure_firestore(mock_get_client)
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
            self.assertEqual(response.json().get("registration_id"), mock_doc.id)
            mock_client.collection.assert_called_with("training_registrations")

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
