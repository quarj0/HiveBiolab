import logging

from django.db import DatabaseError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from hivebiolab.api_helpers import (
    parse_json_body,
    json_error,
    json_success,
    get_client_metadata,
)

from .models import NewsletterSubscriber

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

    try:
        subscriber = NewsletterSubscriber.objects.create(
            email=email,
            name=(payload.get("name") or "").strip(),
            source=(payload.get("source") or "").strip(),
            metadata=metadata,
        )
    except DatabaseError as exc:  # pragma: no cover - DB failure
        logger.exception("Failed to persist newsletter subscription.", exc_info=exc)
        return json_error(
            "Unable to save the subscription right now. Please try again.", status=500
        )

    return json_success(
        "Subscription received. We'll keep you posted!",
        status=201,
        extra={"subscription_id": subscriber.pk},
    )
