# -*- coding: utf-8 -*-
"""Django settings for where_is_my_stuff_api project.

see: https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import print_function, unicode_literals

# Standard Library
import sys
from email.utils import getaddresses
import datetime

# Third Party Stuff
import environ
from kombu import Exchange, Queue
from django.utils.translation import ugettext_lazy as _

ROOT_DIR = environ.Path(__file__) - 2  # (/a/b/myfile.py - 2 = /a/)
BASE_DIR = ROOT_DIR.path('where_is_my_stuff')
sys.path.append(BASE_DIR.path('apps').root,)

env = environ.Env()

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# People who get code error notifications.
# In the format 'Full Name <email@example.com>, Full Name <anotheremail@example.com>'
ADMINS = getaddresses([env("DJANGO_ADMINS", default='where_is_my_stuff_api Admin <admin@example.com>')])

# Not-necessarily-technical managers of the site. They get broken link
# notifications and other various emails.
MANAGERS = ADMINS

# INSTALLED APPS
# ==========================================================================
# List of strings representing installed apps.
# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = (
    # django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.gis',
    # 'django.contrib.humanize',  # Useful template tags

    # third-party apps
    'rest_framework',  # http://www.django-rest-framework.org/
    'rest_framework.authtoken',  # http://www.django-rest-framework.org/
    'rest_auth',  # https://github.com/Tivix/django-rest-auth
    'rest_auth.registration',  # https://github.com/Tivix/django-rest-auth
    'versatileimagefield',  # https://github.com/WGBH/django-versatileimagefield/
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'axes',

    # project apps
    'base',
    'users',
    'stuff',
)

# INSTALLED APPS CONFIGURATION
# ==========================================================================

# django.contrib.auth
# ------------------------------------------------------------------------------
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'users.validators.HasUpperValidator'
    },
    {
        'NAME': 'users.validators.HasLowerValidator'
    },
    {
        'NAME': 'users.validators.HasDigitValidator'
    },
    {
        'NAME': 'users.validators.HasSpecialCharacterValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
]

# rest_framework
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'base.api.pagination.PageNumberPagination',
    'PAGE_SIZE': 30,

    # 'Accept' header based versioning
    # http://www.django-rest-framework.org/api-guide/versioning/
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION': '1.0',
    'ALLOWED_VERSIONS': ['1.0', ],
    'VERSION_PARAMETER': 'version',

    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS': 'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # switch this for all but simple projects
        # 'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10000/day',
    },
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',

        # Mainly used for api debug.
        'rest_framework.authentication.SessionAuthentication',

        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    "EXCEPTION_HANDLER": "base.exceptions.exception_handler",
}
# django.contrib.sites
# ------------------------------------------------------------------------------
SITE_ID = 1
SITES = {
    SITE_ID: {"domain": "localhost:8000", "scheme": "http", "name": "localhost"},
}


# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
# List of middleware classes to use.  Order is important; in the request phase,
# this middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# DJANGO CORE
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
# Defaults to false, which is safe, enable them only in development.
DEBUG = env.bool('DJANGO_DEBUG', False)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# Languages we provide translations for
LANGUAGES = (
    ("en", _("English")),
)

# A tuple of directories where Django looks for translation files.
LOCALE_PATHS = (
    str(BASE_DIR.path("locale")),
)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# The list of directories to search for fixtures
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    str(BASE_DIR.path('fixtures')),
)

# The Python dotted path to the WSGI application that Django's internal servers
# (runserver, runfcgi) will use. If `None`, the return value of
# 'django.core.wsgi.get_wsgi_application' is used, thus preserving the same
# behavior as previous versions of Django. Otherwise this should point to an
# actual WSGI application object.
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'

# URL CONFIGURATION
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'where_is_my_stuff.urls'

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.smtp.EmailBackend')

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': env.db("DATABASE_URL", default="postgres://localhost/where_is_my_stuff"),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['CONN_MAX_AGE'] = 10
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

# TEMPLATE CONFIGURATION
# -----------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(BASE_DIR.path('templates')),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                # Your stuff: custom template context processors go here
            ],
        },
    },
]

# STATIC FILE CONFIGURATION
# -----------------------------------------------------------------------------
# Absolute path to the directory static files should be collected to.
# Example: "/var/www/example.com/static/"
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR.path('.staticfiles'))

# URL that handles the static files served from STATIC_ROOT.
# Example: "http://example.com/static/", "http://static.example.com/"
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# A list of locations of additional static files
STATICFILES_DIRS = (
    str(BASE_DIR.path('static')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(ROOT_DIR.path('.media'))

# URL that handles the media served from MEDIA_ROOT.
# Examples: "http://example.com/media/", "http://media.example.com/"
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = "slugify.slugify"

#  SECURITY
# -----------------------------------------------------------------------------
CSRF_COOKIE_HTTPONLY = False  # Allow javascripts to read CSRF token from cookies
SESSION_COOKIE_HTTPONLY = True  # Do not allow Session cookies to be read by javascript

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

JWT_EXPIRATION_MINS = env.int("JWT_EXPIRATION_MINS", default=1440)
JWT_REFRESH_DAYS = env.int("JWT_REFRESH_DAYS", default=90)
LOGIN_ATTEMPTS = env.int("LOGIN_ATTEMPTS", default=10)
LOGIN_TIMEOUT_SECS = env.int("LOGIN_TIMEOUT_SECS", default=300)

# ALLAUTH
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
LOGIN_REDIRECT_URL = '/'
ACCOUNT_PASSWORD_MIN_LENGTH = 0  # disable in allauth in favor of native django validators
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = LOGIN_ATTEMPTS
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = LOGIN_TIMEOUT_SECS

# DJANGO-AXES
AXES_LOGIN_FAILURE_LIMIT = LOGIN_ATTEMPTS
AXES_COOLOFF_TIME = datetime.timedelta(seconds=LOGIN_TIMEOUT_SECS)

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=JWT_REFRESH_DAYS),
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=JWT_EXPIRATION_MINS),
}

# DJANGO-REST-AUTH
REST_AUTH_SERIALIZERS = {
    'JWT_SERIALIZER': 'users.serializers.JWTSerializer',
    'USER_DETAILS_SERIALIZER': 'users.serializers.UserDetailsSerializer',
    'LOGIN_SERIALIZER': 'users.serializers.LoginSerializer',
}

# use JWT
REST_USE_JWT = True

# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# Default logging for Django. This sends an email to the site admins on every
# HTTP 500 error. Depending on DEBUG, all other log records are either sent to
# the console (DEBUG=True) or discarded by mean of the NullHandler (DEBUG=False).
# See http://docs.djangoproject.com/en/dev/topics/logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'complete': {
            'format': '%(levelname)s:%(asctime)s:%(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s:%(asctime)s: %(message)s'
        },
        'null': {
            'format': '%(message)s',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Redis
REDIS_SETTINGS = {
    'HOST': env('REDIS_HOST', default='127.0.0.1'),
    'PORT': env.int("REDIS_PORT", default=6379),
    'DB_CELERY_BROKER': env.int("REDIS_DB_CELERY_BROKER", default=7),
    'DB_CELERY_RESULT': env.int("REDIS_DB_CELERY_RESULT", default=7),
}

# Celery
BROKER_URL = env('REDIS_URL', default='redis://{}:{}/{}'
                 .format(REDIS_SETTINGS['HOST'],
                         REDIS_SETTINGS['PORT'],
                         REDIS_SETTINGS['DB_CELERY_BROKER']))

CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_IGNORE_RESULT = True
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_EVENT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = env('REDIS_URL', default='redis://{}:{}/{}'
                            .format(REDIS_SETTINGS['HOST'],
                                    REDIS_SETTINGS['PORT'],
                                    REDIS_SETTINGS['DB_CELERY_RESULT']))
CELERY_DEFAULT_ROUTING_KEY = 'where_is_my_stuff'
CELERYBEAT_SCHEDULE_FILENAME = '/tmp/where_is_my_stuff-celerybeat-schedule'
CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('default', Exchange('default')),
    # Queue('long_tasks', Exchange('long_tasks')),
)
CELERY_ALWAYS_EAGER = False  # "True" to skip celery daemon
