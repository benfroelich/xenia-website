"""
Django settings for froelich_leon project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from .settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# send email to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CRISPY_FAIL_SILENTLY = not DEBUG

# currently disabled because wagtail is using non-standard-conforming
# html (though it renders fine)
HTMLVALIDATOR_ENABLED = False
HTMLVALIDATOR_OUTPUT = 'file'
HTMLVALIDATOR_FAILFAST = True
HTMLVALIDATOR_VNU_JAR = '~/Downloads/vnu.jar'

if HTMLVALIDATOR_ENABLED:
    MIDDLEWARE += ("htmlvalidator.middleware.HTMLValidator",)

USE_S3 = True
if USE_S3:
    from .aws_settings import *
else:
    # just serve user-uploaded files locally
    import os
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

