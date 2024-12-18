"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""


import os.path
import sys
from pathlib import Path
import base64
from dotenv import dotenv_values


###############################################################################
#                   Configuração das variáveis de ambientes                   #
###############################################################################

SECRETS = dotenv_values('/run/secrets/env_projeto_django')
if not SECRETS:
    SECRETS = dotenv_values(
        f'{Path(__file__).resolve().parent.parent.parent}/dotenv_files/.env')
    if not SECRETS:
        from io import StringIO
        SECRETS_VAR_ENV_BASE64 = base64.b64decode(
            os.getenv('SECRETS_VAR_ENV_BASE64', '').encode()).decode()
        SECRETS = dotenv_values(stream=StringIO(SECRETS_VAR_ENV_BASE64))
        if not SECRETS:
            exit()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


DATA_DIR = BASE_DIR.parent / 'staticfiles'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRETS['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv('DEBUG', False):
    DEBUG = bool(int(os.getenv('DEBUG', '0')))
else:
    DEBUG = bool(int(SECRETS['DEBUG']))


if os.getenv('TESTE', False):
    TESTE = bool(int(os.getenv('TESTE', '0')))
else:
    TESTE = bool(int(SECRETS['TESTE']))

ALLOWED_HOSTS = [
    h.strip() for h in SECRETS['ALLOWED_HOSTS'].split(',')
    if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    h.strip() for h in SECRETS['CSRF_TRUSTED_ORIGINS'].split(',')
    if h.strip()
]
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "fontawesomefree",
    "home.apps.HomeConfig",

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR/'templates'
        ],
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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


if TESTE and DEBUG:

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": SECRETS['DB_ENGINE'],
            "NAME": SECRETS['POSTGRES_DB'],
            "USER": SECRETS['POSTGRES_USER'],
            "PASSWORD": SECRETS['POSTGRES_PASSWORD'],
            "HOST": SECRETS['POSTGRES_HOST'],
            "PORT": SECRETS['POSTGRES_PORT'],
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = DATA_DIR / 'static'

media_URL = "/media/"
media_ROOT = DATA_DIR / 'static/media'

STATICFILES_DIRS = [
    DATA_DIR,
    BASE_DIR / 'static',
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, '../apps'))

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
