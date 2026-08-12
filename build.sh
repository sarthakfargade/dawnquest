#!/usr/bin/env bash
# Render runs this on every deploy.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create a superuser automatically if one doesn't already exist, using
# credentials from environment variables (set these in Render's dashboard).
# Safe to re-run on every deploy -- does nothing if the user already exists.
python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
if username and password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Created superuser: {username}')
else:
    print('Superuser already exists or env vars not set, skipping.')
"

# Load the scraped sample questions into the live database (safe to re-run,
# get_or_create means it won't duplicate on subsequent deploys).
python manage.py ingest_questions