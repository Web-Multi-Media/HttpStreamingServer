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

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

ALLOWED_HOSTS = ['web', 'localhost']

if os.getenv('DEPLOY_ENV', 'dev') == 'production':
    DEBUG = False
    VERBOSE_OUTPUT = False
    ALLOWED_HOSTS.append(os.getenv('HTTPSTREAMING_HOST', ''))
    VIDEO_URL = '/Videos/'
    STATICFILES_DIRS = (os.path.join(BASE_DIR, '../frontend/build/static/'))
else:
    DEBUG = True
    VERBOSE_OUTPUT = True
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
        'debug_toolbar.panels.sql.SQLPanel',
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


if (VERBOSE_OUTPUT is True):
    customstdout = subprocess.PIPE
    customstderr = subprocess.PIPE
else:
    customstdout = subprocess.DEVNULL
    customstderr = subprocess.DEVNULL

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/



# Application definition

INSTALLED_APPS = [
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
    'rest_auth.registration',
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
    'StreamingServer.middleware.UserAuthMiddleware',
]

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
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
# if 'test' in sys.argv:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': ':memory:',
#         }
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#         }
#     }
#
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
    'PAGE_SIZE': 10
}

# https://django-rest-auth.readthedocs.io/en/latest/installation.html#registration-optional
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = 'none'
