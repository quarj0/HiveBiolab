# HiveBiolab Backend

This Django service implements the API surface that `hive-bio` will reach out to when it needs persistence or notifications. The project stores incoming submissions—newsletter signups, contact messages, and training registrations—in Firestore so the frontend team can deploy the static assets anywhere (Vite, Cloud Run, etc.) without bundling persistence.

## Getting started

1. Create a Python virtual environment (Python 3.10+) and install the pinned dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env`, fill in real values for your Firebase project/hosts, and keep the actual `.env` file out of source control.
3. Run database migrations (even though Firestore stores the data, Django still expects migrations for future models).

   ```bash
   python manage.py migrate
   ```

4. Start the dev server:

   ```bash
   python manage.py runserver
   ```

## Configuration

| Variable | Description | Default |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Django secret key used in production (keep it secret). | `django-insecure-d2=...` |
| `DJANGO_DEBUG` | Debug flag (`false` in production). | `true` |
| `DJANGO_ALLOWED_HOSTS` | Space-separated hosts allowed (`example.com api.example.com`). | `*` |
| `FRONTEND_ORIGINS` | Space-separated frontend origins for CORS. Set to `*` to allow all. | `http://localhost:5173` |
| `CSRF_TRUSTED_ORIGINS` | Override for CSRF trusted origins (defaults to `FRONTEND_ORIGINS`). | (see above) |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to the Firebase service-account JSON (local only). Leave empty to let `kumasihivewebsite-service.json` in the repo root do the job. | `kumasihivewebsite-service.json` |
| `JAZZMIN_SITE_TITLE` | Text shown in the browser title bar of the admin. | `HiveBiolab Admin` |
| `JAZZMIN_SITE_HEADER` | Header text that appears inside the Jazzmin layout. | `HiveBiolab` |
| `JAZZMIN_SITE_BRAND` | Branding text in the sidebar. | `HiveBiolab` |
| `JAZZMIN_WELCOME_SIGN` | Welcome message that shows on the admin index page. | `Review newsletter, contact, and training requests` |
| `JAZZMIN_COPYRIGHT` | Footer text shown in the Jazzmin layout. | `HiveBiolab © 2025` |

`python-dotenv` automatically loads the `.env` file when Django boots, so any env var you place there is available to the settings module.

When deployed to Cloud Run with a service account that has Firestore access, you can omit `GOOGLE_APPLICATION_CREDENTIALS` and rely on Application Default Credentials.

## Environment file

- Copy `.env.example` to `.env` and update it with your secrets (service account path, allowed hosts, CORS origins, Jazzmin labels, etc.).
- `.env` is loaded automatically by `python-dotenv`, so each `manage.py` invocation and Cloud Run container sees the same configuration.
- If you keep a service account JSON named `kumasihivewebsite-service.json` at the project root, `firebase-admin` will load it automatically when `GOOGLE_APPLICATION_CREDENTIALS` is unset, but you can still point to a different file by overriding the env var.

## Firestore collections

- `newsletter_subscribers`
- `contact_messages`
- `training_registrations`

Each document automatically receives `created_at` (Firestore server timestamp) and metadata fields such as `ip_address` and `user_agent`.

## API endpoints

Use the JSON payloads below when the Vite app submits data. All endpoints accept `POST` only, return JSON, and respond with `detail` plus the created document `id`.

### `POST /api/newsletter/subscribe/`

Payload:

```json
{
  "email": "researcher@hive.com",
  "name": "Kwaku Mensah",
  "source": "homepage"
}
```

Response:

```json
{
  "detail": "Subscription received. We'll keep you posted!",
  "subscription_id": "docKey123"
}
```

### `POST /api/contact/`

Payload:

```json
{
  "name": "Amina Adom",
  "email": "amina@example.com",
  "subject": "Training inquiry",
  "message": "Interested in the molecular biology workshop."
}
```

Response:

```json
{
  "detail": "Thanks for reaching out! We will respond as soon as possible.",
  "message_id": "msgKey123"
}
```

### `POST /api/training/register/`

Payload:

```json
{
  "full_name": "Fred Boateng",
  "email": "fred@hive.org",
  "program": "Bioinformatics & Data Analysis",
  "phone": "+233501234567",
  "experience": "Python scripting, basic genomics",
  "goals": "Build pipelines for AMR tracking"
}
```

Response:

```json
{
  "detail": "Registration received. Our team will reach out with next steps.",
  "registration_id": "regKey123"
}
```

## Testing

```
python manage.py test
```

## Deployment notes

- Run `python manage.py collectstatic` and serve the `staticfiles` directory if you plan to host static assets from Django.
- When building a Cloud Run service, set the same environment variables in the service configuration and ensure the attached service account has Firestore read/write access.
