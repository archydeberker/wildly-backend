deploy: python scripts/get_credentials_from_s3.py
deploy: flask db upgrade
web: gunicorn app:app