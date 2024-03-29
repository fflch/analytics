from email.policy import default
import os
from decouple import config
from unipath import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = [config('ALLOWED_HOSTS')]

AUTH_USER_MODEL= 'accounts.UserModel'

OAUTH_CALLBACK_ID = config('OAUTH_CALLBACK_ID')

AUTHLIB_OAUTH_CLIENTS = {
    'usp': {
        'client_id': config('OAUTH_CLIENT_ID'),
        'client_secret': config('OAUTH_CLIENT_SECRET_KEY')
    }
}

REDIRECT_AFTER_LOGOUT_URL = ""

REDIRECT_URI = '/auth/authorize'

ALLOWED_UNIDADES = [
    config('ALLOWED_UNIDADES')
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_oauth_usp.accounts',
    'fontawesomefree',
    'debug_toolbar',
    'rest_framework',
    'apps.home',  
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"  
LOGOUT_REDIRECT_URL = "home"  
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/frontend/templates")  

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.home.config.config',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': config('DBNAME'),
        'USER': config('DBUSER'),
        'PASSWORD': config('DBPASSWORD'),
        'HOST': config('DBHOST'),   
        'PORT': config('DBPORT'),
    },
    'etl': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': config('ETL_DBNAME'),
        'USER': config('ETL_DBUSER'),
        'PASSWORD': config('ETL_DBPASSWORD'),
        'HOST': config('ETL_DBHOST'),   
        'PORT': config('ETL_DBPORT'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(CORE_DIR, 'apps/static'),)

if not DEBUG:
    STATIC_ROOT = os.path.join(CORE_DIR, 'static')


INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

if DEBUG:
    import socket 
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]