import os
from pathlib import Path

DARKSKY_API_KEY = os.environ.get("DARKSKY_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
TEST_EMAIL_ACCOUNT = os.environ.get("TEST_EMAIL_ACCOUNT")
DEFAULT_WEIGHTINGS = {'precip_probability': -10,
                      'precip_intensity': -2,
                      'cloud_cover': -5}

S3_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID_WINE')
S3_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY_WINE')
S3_BUCKET_NAME = 'weather-window'

root = Path(__file__).parent.absolute()

GOOGLE_CREDENTIALS_PATH = root / 'credentials.json'
