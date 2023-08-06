from __future__ import absolute_import, unicode_literals

import os
from pathlib import Path
import environ
import platform
import base64

ROOT_DIR = environ.Path(__file__) - 4  # (remo_app/remo_app/config/standalone/settings.py - 4 = remo_app/)
APPS_DIR = ROOT_DIR.path('remo_app')
env = environ.Env()

RUNNING_MODE = 'standalone'
REMO_UUID = env('REMO_UUID', default='undefined')
REMO_STATS_SERVER = env('REMO_STATS_SERVER', default='https://app.remo.ai')

REMO_HOME = env('REMO_HOME', default=str(Path.home().joinpath('.remo')))

DEMO_USERNAME = None

# SECRET CONFIGURATION
s = "{}-142-{}".format(platform.platform(), 'remo')
SECRET_KEY = env('DJANGO_SECRET_KEY', default=str(base64.urlsafe_b64encode(s.encode("utf-8")), "utf-8"))

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    'whitenoise.runserver_nostatic',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
THIRD_PARTY_APPS = (
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
)
LOCAL_APPS = (
    'remo_app.remo.apps.RemoConfig',
)
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'remo_app.remo.api.middleware.LocalUserMiddleware',
    'spa.middleware.SPAMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', False)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
SENDGRID_API_KEY = env('SENDGRID_API_KEY',
                       default='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')
EMAIL_LIST = env('EMAIL_LIST', default=['andrea.larosa@rediscovery.io', 'volodymyr@remo.ai', 'pooja@remo.ai'])

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres://remo:remo@localhost:5432/remo'),
}

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

# STATIC FILE CONFIGURATION
STATIC_URL = '/static/'
STATIC_ROOT = str(APPS_DIR('static'))
DOCS_DIR = os.path.join(STATIC_ROOT, 'docs')
STATICFILES_STORAGE = 'spa.storage.SPAStaticFilesStorage'

# MEDIA CONFIGURATION
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(REMO_HOME, 'media')

# URL Configuration
ROOT_URLCONF = 'remo_app.config.standalone.urls'

WSGI_APPLICATION = 'remo_app.config.standalone.wsgi.application'

# Logging
# ---------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s RemoApp] %(levelname)s - %(message)s',
            'datefmt': '%H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'remo_app': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

# DJANGO REST FRAMEWORK SETTINGS
# ------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.TokenAuthentication',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 32,
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'remo_app.remo.api.views.backend.CustomModelBackend'
]

REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'remo_app.remo.api.serializers.LoginSerializer'
}

# IMAGE SETTINGS
# ------------------------------
THUMBNAIL_SIZE = (50, 50)
PREVIEW_SIZE = (225, 225)
VIEW_SIZE = (1000, 1000)
VIEW_QUALITY = 60
PREVIEW_QUALITY = 60
THUMBNAIL_QUALITY = 95
HIGH_RESOLUTION = (3840, 2160)
HIGH_RESOLUTION_QUALITY = 60
HIGH_RESOLUTION_THRESHOLD = int(HIGH_RESOLUTION[0] * HIGH_RESOLUTION[1] * 1.3) # +30%
HIGH_RESOLUTION_FILE_SIZE_THRESHOLD = 10 * 1024**2   # 10MB
CACHE_RETENTION_PERIOD = 120    # seconds
CACHE_IMAGES_LIMIT = 2

TMP_DIR = os.path.join(REMO_HOME, 'tmp')

IMAGE_MIME_TYPES = {
    'image/jpeg', 'image/png', 'image/jpg', 'image/tiff'
}

IMAGE_FILE_EXTENSIONS = {
    '.jpeg', '.png', '.jpg', '.tiff', '.tif'
}

ANNOTATION_MIME_TYPES = {
    'application/json', 'text/xml', 'text/csv'
}

ANNOTATION_FILE_EXTENSIONS = {
    '.json', '.xml', '.csv'
}

ARCHIVE_MIME_TYPES = {
    'application/zip', 'application/gzip', 'application/x-bzip2', 'application/x-tar', 'application/x-xz'
}

ARCHIVE_FILE_EXTENSIONS = {
    '.zip', '.gz', '.tar', '.tgz', '.tar.gz', '.bz2', '.tar.bz2', '.xz'
}

# 5 GB max file size for upload
MAX_FILE_SIZE = 5 * 1024**3
DATA_UPLOAD_MAX_MEMORY_SIZE = MAX_FILE_SIZE  # to override django default value

# Maximum image size (in bytes) which are automatically downloaded
# from external resource. For example, during annotations upload
MAX_EXTERNAL_DOWNLOAD_IMAGE_SIZE = MAX_FILE_SIZE

# Hubspot API KEY authorization
# Set HUBSPOT_API_KEY to None to disable Hubspot requests
HUBSPOT_API_KEY = env('HUBSPOT_API_KEY', default='5aeb26cd-2515-4681-b2f4-68248ff651a2')
HUBSPOT_API_THROTTLING_RETRIES = 10

KNOWLEDGE_GRAPH_API_KEY = env('KNOWLEDGE_GRAPH_API_KEY', default='AIzaSyC48ajVnypsGl5MnVCp_c2xRVxAUxl0HfM')
USE_KNOWLEDGE_GRAPH_API = env('USE_KNOWLEDGE_GRAPH_API', default=False)
IMAGE_UPLOADING_THREADS = env('IMAGE_UPLOADING_THREADS', default=1)
FEEDBACKS_ACCESS_KEY = env('FEEDBACKS_ACCESS_KEY', default='golden_age')
LOCAL_FILES = '/local-files'
ALLOWED_HOSTS = ['.localhost', '.ngrok.io']
STORAGE = 'local'
