import json
from typing import Any, Dict, Optional

from django.http import JsonResponse, HttpRequest


def parse_json_body(request: HttpRequest) -> Optional[Dict[str, Any]]:
    """Parse the JSON payload from the request body, or return None if invalid."""
    if not request.body:
        return {}

    try:
        return json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def json_error(message: str, status: int = 400) -> JsonResponse:
    return JsonResponse({"detail": message}, status=status)


def json_success(message: str, status: int = 200, extra: Optional[Dict[str, Any]] = None):
    payload: Dict[str, Any] = {"detail": message}
    if extra:
        payload.update(extra)
    return JsonResponse(payload, status=status)


def get_client_metadata(request: HttpRequest) -> Dict[str, Any]:
    forwarded_for = request.headers.get("X-Forwarded-For", "")
    ip_address = (
        forwarded_for.split(",")[0].strip()
        if forwarded_for
        else request.META.get("REMOTE_ADDR")
    )

    return {
        "ip_address": ip_address,
        "user_agent": request.headers.get("User-Agent"),
        "referrer": request.headers.get("Referer"),
        "accept_language": request.headers.get("Accept-Language"),
    }
