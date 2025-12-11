import logging
import os
from pathlib import Path
from typing import Tuple

logger = logging.getLogger(__name__)

_firestore_client = None
_firebase_modules: Tuple = ()


def _load_firebase_modules():
    """Import Firebase Admin modules lazily so we only require them when the API is used."""
    global _firebase_modules
    if _firebase_modules:
        return _firebase_modules

    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
    except ImportError as exc:
        raise RuntimeError(
            "The firebase-admin package is required. Install it with "
            "`pip install firebase-admin`."
        ) from exc

    _firebase_modules = (firebase_admin, credentials, firestore)
    return _firebase_modules


def get_server_timestamp():
    """Expose Firestore's server timestamp sentinel so views can reuse it without importing firebase_admin."""
    _, _, firestore = _load_firebase_modules()
    return firestore.SERVER_TIMESTAMP


def get_firestore_client():
    """Return a cached Firestore client, initializing Firebase if necessary."""
    global _firestore_client
    if _firestore_client is not None:
        return _firestore_client

    firebase_admin, credentials, _ = _load_firebase_modules()
    _initialize_firebase(firebase_admin, credentials)
    _, _, firestore = _load_firebase_modules()
    _firestore_client = firestore.client()
    return _firestore_client


def _initialize_firebase(firebase_admin_module, credentials_module):
    if firebase_admin_module._apps:
        return

    credential_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    try:
        if credential_path:
            credential_file = Path(credential_path)
            if not credential_file.exists():
                raise RuntimeError(
                    f"Firebase credential file not found at {credential_file}"
                )
            firebase_admin_module.initialize_app(
                credentials_module.Certificate(str(credential_file))
            )
        else:
            firebase_admin_module.initialize_app()
    except Exception as exc:  # pragma: no cover - environment-specific
        logger.exception("Unable to initialize Firebase Admin SDK.")
        raise RuntimeError(
            "Could not initialize Firebase. Make sure GOOGLE_APPLICATION_CREDENTIALS "
            "points to a valid service account or that default credentials are available."
        ) from exc
