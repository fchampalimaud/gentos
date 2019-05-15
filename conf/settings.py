"""
Django settings for conf project.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "changeme!")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", False)

ALLOWED_HOSTS = [
    hostname for hostname in os.getenv("ALLOWED_HOSTS", "localhost").split(",")
]

SITE_ID = 1

ADMINS = [
    tuple(admin.split(",")) for admin in os.getenv("ADMINS", "").split(";") if admin
]

MANAGERS = [
    tuple(manager.split(","))
    for manager in os.getenv("MANAGERS", "").split(";")
    if manager
] or ADMINS

# Application definition

INSTALLED_APPS = [
    # local apps
    "congentodb_client",
    # 3rd party apps
    "fishdb.apps.FishDBConfig",
    "flydb",
    "rodentdb.apps.RodentDBConfig",
    "confirm_users",
    "notifications",
    "orquestra",
    "pyforms_web.web",
    "jfu",
    "sorl.thumbnail",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

MIDDLEWARE = [
    "pyforms_web.web.middleware.PyFormsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = "conf.urls"

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
            ]
        },
    }
]

WSGI_APPLICATION = "conf.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("DATABASE_USERNAME"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "HOST": os.getenv("DATABASE_HOST", default="localhost"),
        "PORT": os.getenv("DATABASE_PORT", default=3306),
    },
    "api": {
        "ENGINE": "rest_models.backend",
        "NAME": os.getenv("DATABASE_API_NAME"),
        "USER": os.getenv("DATABASE_API_USERNAME"),
        "PASSWORD": os.getenv("DATABASE_API_PASSWORD"),
        "AUTH": "rest_models.backend.auth.BasicAuth",
        "PREVENT_DISTINCT": False,
    },
}

CONN_MAX_AGE = 60


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Lisbon"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"


# E-mail

EMAIL_HOST = os.getenv("EMAIL_HOST", default="localhost")
EMAIL_PORT = os.getenv("EMAIL_PORT", default=1025)  # Used by MailHog
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", default="webmaster@localhost")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = not DEBUG

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_SUBJECT_PREFIX = "[CONGENTO] "
SERVER_EMAIL = EMAIL_HOST_USER


# django-allauth

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_USERNAME_REQUIRED = False


# django-rest-models

DATABASE_ROUTERS = ["rest_models.router.RestModelRouter"]
