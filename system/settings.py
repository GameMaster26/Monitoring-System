"""
Django settings for system project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from .jasmine import JAZZMIN_SETTINGS,JAZZMIN_UI_TWEAKS
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

""" if os.name == 'nt':
    VENV_BASE = os.environ['VIRTUAL_ENV']
    os.environ['PATH'] = os.path.join(VENV_BASE, 'Lib\\site-packages\\osgeo') + ';' + os.environ['PATH']
    os.environ['PROJ_LIB'] = os.path.join(VENV_BASE, 'Lib\\site-packages\\osgeo\\data\\proj') + ';' + os.environ['PATH'] """


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(x=$$$f(ky8%a(2ei#q3*arlp^^*kw87=zth3dkzty81lrhmd@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    #packages
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'rest_framework',
    'rest_framework_gis',
    

    #installed apps
    'leaflet',
    'djgeojson',
    'monitoring',
    'import_export',
    
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]


ROOT_URLCONF = 'system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates/')],
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

WSGI_APPLICATION = 'system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',#'ENGINE': 'django.contrib.gis.db.backends.mysql',
        'NAME': 'animalbite',
        'USER': 'postgres',
        'PASSWORD': 'Password',
        'PORT': '5432',
        'HOST': 'localhost',
    }
}

#GDAL_LIBRARY_PATH = os.path.join("C:\\", "OSGeo4W", "bin", "geos.dll")
#GDAL_LIBRARY_PATH = os.path.join("C:\\", "OSGeo4W", "bin", "geos_c.dll")
GDAL_LIBRARY_PATH = os.path.join("C:\\", "OSGeo4W", "bin", "gdal309.dll")
GEOS_LIBRARY_PATH = os.path.join("C:\\", "OSGeo4W", "bin", "geos_c.dll")

# GDAL and GEOS library paths for Windows
#GDAL_LIBRARY_PATH = os.getenv("GDAL_LIBRARY_PATH", r"C:\OSGeo4W64\bin\gdal309.dll")
#GEOS_LIBRARY_PATH = os.getenv("GEOS_LIBRARY_PATH", r"C:\OSGeo4W64\bin\geos_c.dll")


SERIALIZATION_MODULES= {
    'geojson':'djgeojson.serializers',
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR,'static'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (11.6400,124.4642),  
    'DEFAULT_ZOOM': 10,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
    'RESET_VIEW': False,
    'TILES': [
        ('Mapbox', 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {'attribution': '&copy; OpenStreetMap contributors'}),
    ],
}



MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
jasmine = JAZZMIN_SETTINGS

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Expire session when browser closes
SESSION_COOKIE_SECURE = False  # Set to True if using HTTPS
SESSION_COOKIE_HTTPONLY = True  # Set to True for security


# Login URL setting to redirect non-authenticated users
LOGIN_URL = '/admin/login/'
AUTH_USER_MODEL = 'monitoring.User'
LOGIN_REDIRECT_URL = '/admin/'  # Redirect to the overview page after login
