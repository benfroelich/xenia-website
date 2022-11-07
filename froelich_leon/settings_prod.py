"""
Django settings for froelich_leon project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from .settings_common import *

IS_HEROKU = "DYNO" in os.environ

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['terravenustalandscapes.com']
if IS_HEROKU:
    ALLOWED_HOSTS += '*'
    #ALLOWED_HOSTS += '.herokuapp.com'

SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True

from .aws_settings import *

EMAIL_PORT = os.environ['MAILGUN_SMTP_PORT']
EMAIL_HOST = os.environ['MAILGUN_SMTP_SERVER']
EMAIL_HOST_USER = os.environ['MAILGUN_SMTP_LOGIN']
EMAIL_HOST_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
EMAIL_USE_TLS = True

if 'DEFAULT_FROM_EMAIL' in os.environ:
    DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']

if 'SERVER_EMAIL' in os.environ:
    SERVER_EMAIL = os.environ['SERVER_EMAIL']

