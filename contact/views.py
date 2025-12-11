import logging

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from hivebiolab.api_helpers import (
    parse_json_body,
    json_error,
    json_success,
    get_client_metadata,
)
from hivebiolab.firebase_client import get_firestore_client, get_server_timestamp

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def submit_message(request):
    payload = parse_json_body(request)
    if payload is None:
        return json_error("Invalid JSON payload.")

    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip()
    message = (payload.get("message") or "").strip()

    if not name or not email or not message:
        return json_error("Name, email, and message are required.")

    metadata = get_client_metadata(request)
    document = {
        "name": name,
        "email": email.lower(),
        "subject": (payload.get("subject") or "General inquiry").strip(),
        "message": message,
        "organization": payload.get("organization"),
        "metadata": metadata,
        "created_at": get_server_timestamp(),
    }

    try:
        client = get_firestore_client()
        collection = client.collection("contact_messages")
        doc_ref, _ = collection.add(document)
    except RuntimeError as exc:
        logger.exception("Firebase initialization failed.", exc_info=exc)
        return json_error(str(exc), status=500)
    except Exception:  # pragma: no cover - network/db
        logger.exception("Failed to persist contact message.")
        return json_error(
            "Unable to submit the form right now. Please try again later.", status=500
        )

    return json_success(
        "Thanks for reaching out! We will respond as soon as possible.",
        status=201,
        extra={"message_id": doc_ref.id},
    )
