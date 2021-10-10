import os
from pathlib import Path

import django_heroku
import sentry_sdk
from decouple import config
from django.conf.locale import en
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = [
    'goim.herokuapp.com',
    'wwww.goim.herokuapp.com',
    'www.goimrecords.company',
    '0.0.0.0',
    '127.0.0.1',
    'https://goim.herokuapp.com/',
    'goimrecords.company',
    'https://goimrecords.company',
    'https://goimrecords.company',
    'https://www.goimrecords.company',

]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_visit',
    'records',
    'captcha',
    # 'gdstorage',
    'storages',
    'django_agenda',
    'django_heroku',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'user_visit.middleware.UserVisitMiddleware',
]

ROOT_URLCONF = 'goim.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'goim.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(str(BASE_DIR), 'data.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': config('ENGINE'),
        'NAME': config('DBNAME'),
        'USER': 'gwzujuygdeblbj',
        'PASSWORD': config('PASSWORD'),
        'HOST': config('HOST'),
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Douala'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Logins

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'login'
LOGOUT_REDIRECT_URL = 'logout'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'static')  # 'data' is my media folder
MEDIA_URL = 'static/'
# email settings

EMAIL_BACKEND = config('EMAIL_BACKEND')
DEFAULT_FROM_EMAIL = 'Go Immigration'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'emails')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
# Google cloud storage
# GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE =

# Changed Authentication

AUTH_USER_MODEL = 'records.GoUser'

sentry_sdk.init(
    dsn=config('dsn'),
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')

# Amazon config
AWS_LOCATION = 'static'
AWS_ACCESS_KEY_ID = 'AKIA2OXRCB4FS53CNV4I'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'go-immigration-records'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.us-east-2.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_DEFAULT_ACL = 'public-read-write'
AWS_S3_FILE_OVERWRITE = True
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'records.storage_backends.MediaStorage'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
