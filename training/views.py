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
def register_participant(request):
    payload = parse_json_body(request)
    if payload is None:
        return json_error("Invalid JSON payload.")

    full_name = (payload.get("full_name") or "").strip()
    email = (payload.get("email") or "").strip()
    program = (payload.get("program") or "").strip()

    if not full_name or not email or not program:
        return json_error("Full name, email, and program choice are required.")

    metadata = get_client_metadata(request)
    document = {
        "full_name": full_name,
        "email": email.lower(),
        "phone": (payload.get("phone") or "").strip(),
        "program": program,
        "current_level": payload.get("current_level"),
        "experience_summary": payload.get("experience"),
        "goals": payload.get("goals"),
        "message": payload.get("message"),
        "metadata": metadata,
        "created_at": get_server_timestamp(),
    }

    try:
        client = get_firestore_client()
        collection = client.collection("training_registrations")
        doc_ref, _ = collection.add(document)
    except RuntimeError as exc:
        logger.exception("Firebase initialization failed.", exc_info=exc)
        return json_error(str(exc), status=500)
    except Exception:  # pragma: no cover - network/db
        logger.exception("Failed to persist training registration.")
        return json_error(
            "Registration failed. Please try again later.", status=500
        )

    return json_success(
        "Registration received. Our team will reach out with next steps.",
        status=201,
        extra={"registration_id": doc_ref.id},
    )
