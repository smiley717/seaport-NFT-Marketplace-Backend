"""
Django settings for quixotic_backend project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import json
import logging
import os
from pathlib import Path
import environ

import dj_database_url
import django_heroku
from django.core.management.utils import get_random_secret_key


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


MAX_CONN_AGE = 600

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
if not env("SECRET_KEY"):
    logging.warning(
        "SETTING A NEW RANDOM SECRET ON THE FLY. THIS SHOULD ONLY BE USED FOR LOCAL TESTING."
    )
SECRET_KEY = get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
# try:
#     DEBUG = bool(int(env("DEBUG")))
# except:
#     DEBUG = bool(env("DEBUG"))
DEBUG = True

DEBUG_TOOLBAR = env("IS_LOCAL")

ALCHEMY_API_KEY = env('ALCHEMY_API_KEY')
AWS_ACCESS_KEY = env('AWS_ACCESS_KEY')
AWS_SECRET_KEY = env('AWS_SECRET_KEY')
BOUNCER_PRIVATE_KEY = env('BOUNCER_PRIVATE_KEY')
BRIDGE_DEPLOYER_KEY = env('BRIDGE_DEPLOYER_KEY')
BRIDGE_DEPLOYER_ADDRESS = env('BRIDGE_DEPLOYER_ADDRESS')
USE_CELERY_PROCESS_TXN = env('USE_CELERY_PROCESS_TXN')
USE_CELERY = env('USE_CELERY')
DATABASE_URL = env('DATABASE_URL')
DATABASE_CONNECTION_POOL_URL = env('DATABASE_CONNECTION_POOL_URL')
MEMCACHEDCLOUD_SERVERS = env('MEMCACHEDCLOUD_SERVERS')
MEMCACHEDCLOUD_PASSWORD = env('MEMCACHEDCLOUD_PASSWORD')
MEMCACHEDCLOUD_USERNAME = env('MEMCACHEDCLOUD_USERNAME')
REDIS_URL = env('REDIS_URL')
IS_LOCAL = env('IS_LOCAL')
NETWORK = env('NETWORK')
IS_EXTERNAL_API = env('IS_EXTERNAL_API')
L2_WS_ALCHEMY_API_KEY= "wss://opt-mainnet.g.alchemy.com/v2/q_d_3EQ2efRDKPvIw9vouYxYtK4qiQQe"
L1_WS_ALCHEMY_API_KEY= "wss://opt-mainnet.g.alchemy.com/v2/q_d_3EQ2efRDKPvIw9vouYxYtK4qiQQe"

# Application definition

INSTALLED_APPS = [
    "scout_apm.django",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "django.contrib.postgres",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_api_key",
    "api",
    "launchpad",
    "batch_processing",
    "django_celery_beat",  # library
]

if DEBUG_TOOLBAR:
    INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG_TOOLBAR:
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

ROOT_URLCONF = "quixotic_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "quixotic_backend.wsgi.application"

# Database Routers
# https://docs.djangoproject.com/en/4.0/ref/settings/#std-setting-DATABASE_ROUTERS
# if env("DATABASE_CONNECTION_POOL_URL") and env(
#     "DATABASE_FOLLOWER_CONNECTION_POOL_URL"
# ):
#     DATABASE_ROUTERS = ["quixotic_backend.router.PrimaryReplicaRouter"]

# Max File Size
# https://docs.djangoproject.com/en/dev/ref/settings/#data-upload-max-memory-size
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760

# API Custom Header
# https://docs.djangoproject.com/en/3.2/ref/request-response/#django.http.HttpRequest.META

API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if env("IS_EXTERNAL_API") or env("IS_METRICS_API"):
    REST_FRAMEWORK = {
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
        "PAGE_SIZE": 20,
        "DEFAULT_PERMISSION_CLASSES": ["rest_framework_api_key.permissions.HasAPIKey"]
        if not env("IS_LOCAL")
        else [
            "rest_framework.permissions.AllowAny",
        ],
        "DEFAULT_THROTTLE_CLASSES": [
            "rest_framework.throttling.AnonRateThrottle",
            "rest_framework.throttling.UserRateThrottle",
            "api.throttles.RabbitHoleThrottle.RabbitHoleThrottle",
        ],
        "DEFAULT_THROTTLE_RATES": {
            "anon": "10/second",
            "user": "20/second",
            "rabbithole": "300/second",
        },
    }
else:
    REST_FRAMEWORK = {
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
        "PAGE_SIZE": 20,
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework.authentication.TokenAuthentication",
        ],
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.IsAuthenticated",
        ]
        if not env("IS_LOCAL")
        else [],
    }

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_KEY")
AWS_STORAGE_BUCKET_NAME = "fanbase-1"
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False

CORS_ALLOW_HEADERS = ["*"]

if DEBUG or env("IS_EXTERNAL_API"):
    CORS_ALLOW_ALL_ORIGINS = True
    ALLOWED_HOSTS = ["*"]
else:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "https://qx.app",
        "https://testnet.qx.app",
        "https://goerli.qx.app",
        "https://quix-mainnet-develop.vercel.app",
        "https://quix-goerli-develop.vercel.app",
        "https://quix-mainnet-git-feature-bridge-init-fanbase-labs.vercel.app",
    ]
    ALLOWED_HOSTS = [
        "http://localhost:3000",
        "https://qx.app",
        "https://testnet.qx.app",
        "https://goerli.qx.app",
        "https://quix-mainnet-develop.vercel.app",
        "https://quix-goerli-develop.vercel.app",
        "https://quix-mainnet-git-feature-bridge-init-fanbase-labs.vercel.app",
    ]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "https://qx.app",
    "https://testnet.qx.app",
    "https://goerli.qx.app",
    "https://quix-mainnet-develop.vercel.app",
    "https://quix-goerli-develop.vercel.app",
    "https://quix-mainnet-git-feature-bridge-init-fanbase-labs.vercel.app",
]

ADMINS = [
    # Insert your admins here
]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

def get_cache():
    import os

    if (
        env("MEMCACHEDCLOUD_SERVERS")
        and env("MEMCACHEDCLOUD_USERNAME")
        and env("MEMCACHEDCLOUD_PASSWORD")
    ):
        return {
            "default": {
                "BACKEND": "django_bmemcached.memcached.BMemcached",
                "LOCATION": env("MEMCACHEDCLOUD_SERVERS").split(","),
                "OPTIONS": {
                    "username": env("MEMCACHEDCLOUD_USERNAME"),
                    "password": env("MEMCACHEDCLOUD_PASSWORD"),
                },
            }
        }
    elif env("MEMCACHEDCLOUD_SERVERS"):
        return {
            "default": {
                "BACKEND": "django_bmemcached.memcached.BMemcached",
                "LOCATION": env("MEMCACHEDCLOUD_SERVERS").split(","),
                "OPTIONS": {"username": "default"},
            }
        }
    else:
        return {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}


CACHES = get_cache()

# Celery Configuration Options
CELERY_TIMEZONE = "America/Los_Angeles"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_WORKER_CONCURRENCY = 8
CELERY_ACKS_LATE = True

CELERY_IMPORTS = (
    "batch_processing.tasks.token.tasks",
    "batch_processing.tasks.collection.tasks",
    "batch_processing.tasks.common.tasks",
    "batch_processing.tasks.scheduler.tasks",
)

if DEBUG_TOOLBAR:
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: True,
    }
    INTERNAL_IPS = [
        "127.0.0.1",
    ]
