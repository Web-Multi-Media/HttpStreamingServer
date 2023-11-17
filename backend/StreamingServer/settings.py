"""
Django settings for StreamingServer project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os, sys
import dj_database_url
import subprocess
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from filebrowser.sites import site

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


STATIC_URL = '/static/'
STATIC_ROOT = '/usr/static/'

ALLOWED_HOSTS = ['web', 'localhost']


if os.getenv('DEPLOY_ENV', 'dev') == 'production':
    DEBUG = False
    ALLOWED_HOSTS.append(os.getenv('HTTPSTREAMING_HOST', ''))
    VIDEO_URL = '/Videos/'
    STATICFILES_DIRS = (os.path.join(BASE_DIR, '../frontend/build/static/'),)
else:
    DEBUG = True
    VIDEO_URL = 'http://localhost:1337/Videos/'
    INTERNAL_IPS = ['127.0.0.1']

    # Normally django debug toolbar uses `INTERNAL_IPS` to check if it should show, but in
    # docker request.META.REMOTE_ADDR is set to an internal docker IP instead of 127.0.0.1.
    # We hard-code it on for development.
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: True,
    }

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        #'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel'
    ]

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '')


VIDEO_ROOT = os.path.join(BASE_DIR, 'Videos/')

SUBPROCESS_VERBOSE_OUTPUT = (os.getenv('SUBPROCESS_VERBOSE_OUTPUT', 'False') == 'True')

if SUBPROCESS_VERBOSE_OUTPUT:
    customstdout = None
    customstderr = None
else:
    customstdout = subprocess.PIPE
    customstderr = subprocess.STDOUT

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'StreamingServer',
    'StreamServerApp',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'StreamingServer.middleware.UserAuthMiddleware',
]

SITE_ID = 1

ROOT_URLCONF = 'StreamingServer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../frontend/build/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'StreamingServer.wsgi.application'

# Database
DATABASE_URL_ENV_NAME = 'DJANGO_DATABASE_URL'
DATABASES = {'default': dj_database_url.config(
    DATABASE_URL_ENV_NAME, default='postgres://postgres:postgres@db/streaming_server')}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

FIXTURE_DIRS =  ['/usr/src/app/StreamServerApp/fixtures/']

# CORS Config
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
     # the page size must be greater (strictly) than SLIDES_OF_CAROUSEL in VideoCarouselSlick.js
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'SESSION_LOGIN': False
}

# https://django-rest-auth.readthedocs.io/en/latest/installation.html#registration-optional
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_SESSION_REMEMBER = True


sentry_dsn = os.getenv('SENTRY_DSN', None)
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[DjangoIntegration()],

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

# celery
CELERY_BROKER_URL = 'redis://redis:6380'
CELERY_RESULT_BACKEND = 'redis://redis:6380'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6380/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "example"
    }
}

if os.getenv('DEPLOY_BEHIND_PROXY') == 'true':
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

#site.storage.location = "/usr/torrent/"
#site.directory = "/"