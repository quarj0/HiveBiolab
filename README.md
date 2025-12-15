# HiveBiolab Backend

This Django service implements the API surface that `hive-bio` reaches out to when it needs persistence or notifications. Incoming submissions—newsletter signups, contact messages, and training registrations—are stored in Django models backed by the configured SQL database (SQLite by default), so you can review them using the admin at `/admin/` or query them directly from the database.

## Getting started

1. Create a Python virtual environment (Python 3.10+) and install the pinned dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy the provided `.env` file or create a new one (*keep it out of source control*) and update it with host/CORS settings plus real secrets such as `SECRET_KEY`. The file is automatically loaded by `python-dotenv`.
3. Run Django migrations so the `contact`, `newsletter`, and `training` tables exist.

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
| `SECRET_KEY` | Django secret key (must be kept secret in production). | (set a long random value per environment) |
| `DEBUG` | Disable for production (`false`); `true` enables Django’s error pages locally. | `false` |
| `ALLOWED_HOSTS` | Space-separated hosts allowed to serve the API. | `*` |
| `FRONTEND_ORIGINS` | Space-separated origins that can make CORS requests. | `https://biolab.kumasihive.com` |
| `CSRF_TRUSTED_ORIGINS` | Origins allowed to bypass the CSRF origin check (defaults to `FRONTEND_ORIGINS`). | (see above) |
| `JAZZMIN_SITE_TITLE` | Browser title for the admin. | `HiveBiolab Admin` |
| `JAZZMIN_SITE_HEADER` | Header text inside the admin layout. | `HiveBiolab` |
| `JAZZMIN_SITE_BRAND` | Branding text shown in the sidebar. | `HiveBiolab` |
| `JAZZMIN_WELCOME_SIGN` | Welcome message on the admin index page. | `Review newsletter, contact, and training requests` |
| `JAZZMIN_COPYRIGHT` | Footer text shown in Jazzmin. | `HiveBiolab © 2025` |

`python-dotenv` automatically loads the `.env` file when Django boots, so any env var you place there is visible to the settings module.

## Environment file

- Copy the provided `.env` (or create a new one) and populate it with sensible host, CORS, and Jazzmin labels plus secrets such as `SECRET_KEY`. Keep that file out of version control.
- Each `manage.py` invocation and Cloud Run container sees the same configuration thanks to `python-dotenv`.

## Stored data

- `ContactMessage` stores incoming contact forms (name, email, subject, message, optional organization) plus metadata.
- `NewsletterSubscriber` stores subscription requests (email, name, source) and metadata.
- `TrainingRegistration` captures training interest (name, email, phone, program, optional background/goals) and metadata.
- Metadata includes headers such as `ip_address`, `user_agent`, `referrer`, and `accept_language`, and every record has `created_at`.

## API endpoints

Use the JSON payloads below when the Vite app submits data. All endpoints accept `POST` only, return JSON, and respond with `detail` plus the created record `id`.

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
  "subscription_id": 1
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
  "message_id": 1
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
  "registration_id": 1
}
```

## Testing

```
python manage.py test
```

## Deployment notes

- Run `python manage.py collectstatic` and serve the `staticfiles` directory if you host static assets from Django.
- Run `python manage.py migrate` before the service goes live so the tables exist in the production database.
- When deploying, set the same environment variables in the service configuration (especially hosts and CORS origins) and keep `DEBUG=False`.
