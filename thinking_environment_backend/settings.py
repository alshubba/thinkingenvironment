"""
Django settings for thinking_environment_backend project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} env variable".format(var_name)
        if DEBUG:
            warnings.warn(error_msg)
        else:
            raise ImproperlyConfigured(error_msg)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#uo26d&&oe-7_lvb19=1o=-v0sl_%04mv394q^r-3uk3r4-c31'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'easy_thumbnails',
    'rest_framework',
    'rest_framework.authtoken',
    'push_notifications',
    'storages',
    'tems'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':(
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        ),
    'DEFAULT_PERMISSION_CLASSES':(
        'rest_framework.permissions.IsAuthenticated',
        ),
}

PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": "[your api key]",
    "GCM_API_KEY": "AIzaSyC_hz1u5cZeOFzsPi7mG4fdJMy127XPTwk",
    "GCM_ERROR_TIMEOUT": 1000,
    "APNS_CERTIFICATE": os.path.join(BASE_DIR, 'tems/apns-cert-prod.pem'),
    "APNS_TOPIC": "com.alshubba.ThinkingEnvironmentApp",
    "WNS_PACKAGE_SECURITY_ID": "[your package security id, e.g: 'ms-app://e-3-4-6234...']",
    "WNS_SECRET_KEY": "[your app secret key, e.g.: 'KDiejnLKDUWodsjmewuSZkk']",
    "UPDATE_ON_DUPLICATE_REG_ID": True,
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'thinking_environment_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'thinking_environment_backend.wsgi.application'

THUMBNAIL_ALIASES = {
    '': {
        'thumbnail': {'size': (200, 200), 'crop': True},
    },
}

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = 'znapqlakqptfhvts' #my gmail password
EMAIL_HOST_USER = 'thinking.environment@gmail.com' #my gmail username
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Riyadh'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
LOGIN_URL = '/tems/login/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

#MEDIA_ROOT = os.path.join(BASE_DIR,'media')

MEDIA_ROOT = '/media/'

#MEDIA_URL = '/media/'

# AMAZON AWS S3 FOR STORING MEDIA FILES


AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = 'AKIAI2H7ZZCVF6HTZQNA'
AWS_SECRET_ACCESS_KEY = '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'
S3_BUCKET = 'thinkingenvironment'
AWS_STORAGE_BUCKET_NAME = S3_BUCKET
MEDIA_URL = "https://s3.amazonaws.com/%s/" % S3_BUCKET
DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"
THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE
