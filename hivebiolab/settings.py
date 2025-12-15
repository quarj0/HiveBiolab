import sys
from pathlib import Path

import dj_database_url
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


# ─────────────────────────────
# Core security
# ─────────────────────────────

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)
TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

ALLOWED_HOSTS = [
    host.strip()
    for host in config("ALLOWED_HOSTS", default="api.biolab.kumasihive.com")
    .replace(",", " ")
    .split()
    if host.strip()
]


# ─────────────────────────────
# CORS / CSRF
# ─────────────────────────────

FRONTEND_ORIGINS_SETTING = config(
    "FRONTEND_ORIGINS", "https://biolab.kumasihive.com"
).strip()

ALLOW_ALL_ORIGINS = FRONTEND_ORIGINS_SETTING == "*"

CORS_ALLOW_CREDENTIALS = True

if ALLOW_ALL_ORIGINS:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOWED_ORIGINS = []
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [
        origin for origin in FRONTEND_ORIGINS_SETTING.split() if origin
    ]

CSRF_TRUSTED_ORIGINS = [
    origin
    for origin in config("CSRF_TRUSTED_ORIGINS", FRONTEND_ORIGINS_SETTING).split()
    if origin
]


# ─────────────────────────────
# Production security (HTTPS)
# ─────────────────────────────

if not DEBUG and not TESTING:
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"

    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_HTTPONLY = True

    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# ─────────────────────────────
# Applications
# ─────────────────────────────

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "training",
    "newsletter",
    "contact",
]


# ─────────────────────────────
# Middleware
# ─────────────────────────────

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "hivebiolab.urls"

WSGI_APPLICATION = "hivebiolab.wsgi.application"


# ─────────────────────────────
# Templates
# ─────────────────────────────

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ─────────────────────────────
# Database (SQLite – valid for single-instance)
# ─────────────────────────────

if TESTING:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
else:
    DATABASES = {
        "default": dj_database_url.config(
            default=config("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True,
        )
    }


# ─────────────────────────────
# Auth / i18n
# ─────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ─────────────────────────────
# Static files
# ─────────────────────────────

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ─────────────────────────────
# Jazzmin
# ─────────────────────────────

JAZZMIN_SETTINGS = {
    "site_title": "HiveBiolab Admin",
    "site_header": "HiveBiolab",
    "site_brand": "HiveBiolab",
    "welcome_sign": "Manage newsletter, contact, and training submissions",
    "copyright": "HiveBiolab © 2025 • Trusted Biotech",
    "order_with_respect_to": ["training", "newsletter", "contact"],
    "icons": {
        "training": "fas fa-microscope",
        "newsletter": "fas fa-envelope-open-text",
        "contact": "fas fa-comments",
    },
}
