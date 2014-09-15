from .common_settings import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

# DJANGO-DEBUG-TOOLBAR CONFIGURATION
INSTALLED_APPS += (
    'debug_toolbar',
)

TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'en'

# IPs allowed to see django-debug-toolbar output.
INTERNAL_IPS = ('127.0.0.1',)

# END DJANGO-DEBUG-TOOLBAR CONFIGURATION

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': normpath(join(DJANGO_ROOT, 'possum.db')),
        # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        # Empty for localhost through domain sockets or '127.0.0.1' for localhost
        # through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}
