import os

DARKSKY_API_KEY = os.environ.get("DARKSKY_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
TEST_EMAIL_ACCOUNT = os.environ.get("TEST_EMAIL_ACCOUNT")
DEFAULT_WEIGHTINGS = {'precip_probability': -10,
                      'precip_intensity': -2,
                      'cloud_cover': -5}