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
def subscribe(request):
    payload = parse_json_body(request)
    if payload is None:
        return json_error("Invalid JSON payload.")

    email = (payload.get("email") or "").strip().lower()
    if not email or "@" not in email:
        return json_error("A valid email address is required.")

    metadata = get_client_metadata(request)
    document = {
        "email": email,
        "name": (payload.get("name") or "").strip(),
        "source": payload.get("source"),
        "metadata": metadata,
        "created_at": get_server_timestamp(),
    }

    try:
        client = get_firestore_client()
        collection = client.collection("newsletter_subscribers")
        doc_ref, _ = collection.add(document)
    except RuntimeError as exc:
        logger.exception("Unable to initialize Firestore.", exc_info=exc)
        return json_error(str(exc), status=500)
    except Exception:  # pragma: no cover - network/db
        logger.exception("Failed to persist newsletter subscription.")
        return json_error(
            "Unable to save the subscription right now. Please try again.", status=500
        )

    return json_success(
        "Subscription received. We'll keep you posted!",
        status=201,
        extra={"subscription_id": doc_ref.id},
    )
