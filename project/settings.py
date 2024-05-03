"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!

# Get the DEBUG setting from environment variable
# This code sets DEBUG to True if the value of the environment variable DEBUG
# is 'True' (case-sensitive), and False otherwise.
DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.authors",
    "apps.quotes",
    "apps.accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    "postgresql-remote": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRESQL_REMOTE_DB_NAME"),
        "USER": os.getenv("POSTGRESQL_REMOTE_DB_USER"),
        "PASSWORD": os.getenv("POSTGRESQL_REMOTE_DB_PASSWORD"),
        "HOST": os.getenv("POSTGRESQL_REMOTE_DB_HOST"),
        "PORT": os.getenv("POSTGRESQL_REMOTE_DB_PORT"),
    },
    "postgresql-local": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRESQL_LOCAL_DB_NAME"),
        "USER": os.getenv("POSTGRESQL_LOCAL_DB_USER"),
        "PASSWORD": os.getenv("POSTGRESQL_LOCAL_DB_PASSWORD"),
        "HOST": os.getenv("POSTGRESQL_LOCAL_DB_HOST"),
        "PORT": os.getenv("POSTGRESQL_LOCAL_DB_PORT"),
    },
    "mysql-local": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_LOCAL_DB_NAME"),
        "USER": os.getenv("MYSQL_LOCAL_DB_USER"),
        "PASSWORD": os.getenv("MYSQL_LOCAL_DB_PASSWORD"),
    },
}

# LOGGING START

LOGS_DIR = os.path.join(BASE_DIR, "logs")

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "rotating_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "logs.log"),
            "mode": "a",
            "encoding": "utf-8",
            "formatter": "verbose",
            "backupCount": 5,
            "maxBytes": 10485760,
        },
        "console_handler": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "colored",
        },
    },
    "loggers": {
        # unmapped aka root logger, catch logs from ALL modules (files)
        # this would show all of my written logs, like logger.error("hello!")
        "": {
            "level": "DEBUG",
            "handlers": [
                "console_handler",
                "rotating_file_handler",
            ],
        },
        # catch logs from django (make this DEBUG to get loads of info)
        "django": {
            "level": "INFO",
            "handlers": [
                "console_handler",
                "rotating_file_handler",
            ],
            "propagate": False,
        },
        # catch all the SQL that is generated by django's ORM
        "django.db.backends": {
            "level": "INFO",
            "handlers": [
                "console_handler",
                "rotating_file_handler",
            ],
        },
    },
    "formatters": {
        "simple": {
            "format": "{asctime}: {levelname} :: {message}",
            "style": "{",
        },
        "verbose": {
            "format": "{asctime}: {levelname} - {name} {module}.py "
            "(line {lineno:d}) :: {message}",
            "style": "{",
        },
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s %(asctime)s: [%(levelname)s] - %(name)s "
            "%(module)s.py (line %(lineno)s). :: %(message)s",
        },
    },
}

# LOGGING END

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501, pylint: disable=C0301
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: E501, pylint: disable=C0301
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa: E501, pylint: disable=C0301
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa: E501, pylint: disable=C0301
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
