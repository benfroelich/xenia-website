"""
common django settings for the terra venusta project.
"""

import os
from pathlib import Path
import dj_database_url

IS_HEROKU = "DYNO" in os.environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ADMINS = [('benny', 'benfroelich@gmail.com')]
MANAGERS = [('benny', 'benfroelich@gmail.com')]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

WAGTAIL_FRONTEND_LOGIN_TEMPLATE = 'registration/login.html'
WAGTAILADMIN_BASE_URL = 'www.terravenustalandscapes.com'

# currently this is for terravenustalandscapes.com
SITE_ID = 2
# Application definition

LOGIN_REDIRECT_URL = '/profile/'

INSTALLED_APPS = [
    'cmsblog.apps.CmsblogConfig',
    'home.apps.HomeConfig',
    'registration.apps.RegistrationConfig',
    'user_profile.apps.UserProfileConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.humanize',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',

    'modelcluster',
    'taggit',

    'crispy_forms',
    'crispy_bootstrap5',

    'wagtail.contrib.modeladmin',
    'wagtailmenus',
]
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'froelich_leon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtailmenus.context_processors.wagtailmenus',
            ],
        },
    },
]

WSGI_APPLICATION = 'froelich_leon.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'service': 'db_service',
            'passfile': os.environ.get("DJANGO_PG_PASS"),
        },
    }
}

MAX_CONN_AGE = 600

if "DATABASE_URL" in os.environ:
    # Configure Django for DATABASE_URL environment variable.
    DATABASES["default"] = dj_database_url.config(
        conn_max_age=MAX_CONN_AGE, ssl_require=True)

    # Enable test database if found in CI environment.
    if "CI" in os.environ:
        DATABASES["default"]["TEST"] = DATABASES["default"]

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "static-collection"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

WAGTAIL_SITE_NAME = 'Terra Venusta'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CONN_MAX_AGE = None # don't timeout connections
# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-CONN_HEALTH_CHECKS
CONN_HEALTH_CHECK = True

AWS_STORAGE_BUCKET_NAME = "terra-venusta"

# to support wagtail inline preview
X_FRAME_OPTIONS = 'SAMEORIGIN'

EMAIL_BACKEND = 'django_ses.SESBackend'

AWS_ACCESS_KEY_ID = os.environ['AWS_S3_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_S3_SECRET_ACCESS_KEY']
#AWS_SES_CONFIGURATION_SET = 'tv'
AWS_SES_RETURN_PATH = os.environ['AWS_SES_RETURN_PATH']

