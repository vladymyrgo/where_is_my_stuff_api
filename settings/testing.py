from __future__ import absolute_import, unicode_literals

from .development import *  # noqa

MEDIA_ROOT = "/tmp"

SECRET_KEY = 'top-scret!'

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
INSTALLED_APPS += ("tests", )

DEBUG = False
TEMPLATE_DEBUG = False


class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"


# Disable migrations for tests
MIGRATION_MODULES = DisableMigrations()

# Simple hasher for speed
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# simple DB is used to make tests faster
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
    }
}

# To skip celery daemon
CELERY_ALWAYS_EAGER = True
