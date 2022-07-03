from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-vh91q+(iqjs=xi+7354e9u+)&(*se_xcn1-bn4svu$xv*6@ga6"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar',
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE

# ////////////////////////////////////////////////////////////////////////////////

# INTERNAL_IPS for Django Toolbar

INTERNAL_IPS = (
    "127.0.0.1",
    "172.17.0.1"
)

try:
    from .local import *
except ImportError:
    pass
