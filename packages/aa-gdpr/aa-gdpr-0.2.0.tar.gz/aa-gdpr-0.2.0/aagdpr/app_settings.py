from django.conf import settings
from .utils import clean_setting

# Attempt to load JS/CSS/Fonts from staticfiles when possible
# This does not guarantee no CDN usage
# App Developers may or may not respect this setting
AVOID_CDN = clean_setting("AVOID_CDN", False)