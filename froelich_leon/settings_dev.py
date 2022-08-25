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

