# Farm Management System

A multi-user Django app for running a farm: land & fields, crops, livestock (health, production,
breeding), equipment & maintenance, labour (workers & tasks), finance (transactions, categories,
budgets) and compliance (certifications with expiry warnings). Every user only ever sees their own data.

## Quick start (development)

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # set DJANGO_DEBUG=True for local work
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Run the tests: `python manage.py test`

## Configuration (environment variables)

| Variable | Purpose | Default |
|---|---|---|
| `DJANGO_SECRET_KEY` | **Required** when `DJANGO_DEBUG` is off | – |
| `DJANGO_DEBUG` | Never enable in production | `False` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames | – |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | e.g. `https://farm.example.com` | – |
| `DATABASE_URL` | e.g. `postgres://user:pw@host:5432/db` | local SQLite |
| `DJANGO_SECURE_SSL` | HTTPS redirect, secure cookies, HSTS | `True` |
| `DJANGO_ALLOW_REGISTRATION` | Allow public sign-up | `True` |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` | SMTP for password reset; console backend if no user is set | – |
| `DJANGO_LOG_LEVEL` | Log level (stdout) | `INFO` |

## Deploying

```bash
cp .env.example .env     # fill in real values
docker compose up --build -d
docker compose exec web python manage.py createsuperuser
```

The container runs migrations on start and serves with gunicorn on port 8000; static files are served by
WhiteNoise. Put a TLS-terminating reverse proxy (nginx, Caddy, a cloud load balancer) in front, forwarding
`X-Forwarded-Proto`. Point health checks at `/healthz/` (returns 503 if the database is unreachable).

Before go-live run `python manage.py check --deploy`.

## Operations notes

- **Back up the database** (e.g. `pg_dump` on a schedule) – there is no built-in backup.
- Logs go to stdout; collect them with your platform.
- Deleting an animal is a soft delete so its records are preserved.
- Not included: login rate-limiting (put it at the proxy or add `django-axes`), Subresource Integrity
  for the Bootstrap/Font Awesome CDN assets, and error tracking (e.g. Sentry).
