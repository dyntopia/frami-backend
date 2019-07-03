import json
import pathlib
import sys

LOCAL_DIR = pathlib.Path.home() / '.frami'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frami.api',
    'frami.spa',
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
REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}
ROOT_URLCONF = 'frami.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
WSGI_APPLICATION = 'frami.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(LOCAL_DIR / 'db.sqlite3'),
    }
}
VALIDATORS = [
    'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    'django.contrib.auth.password_validation.MinimumLengthValidator',
    'django.contrib.auth.password_validation.CommonPasswordValidator',
    'django.contrib.auth.password_validation.NumericPasswordValidator',
]
AUTH_PASSWORD_VALIDATORS = [{'NAME': v} for v in VALIDATORS]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'

try:
    config = LOCAL_DIR / 'config.json'
    with config.open() as f:
        extra = json.load(f)

    ALLOWED_HOSTS = extra['ALLOWED_HOSTS']
    DEBUG = extra['DEBUG']
    SECRET_KEY = extra['SECRET_KEY']

    if not isinstance(ALLOWED_HOSTS, list):
        raise ValueError('ALLOWED_HOSTS must be a list')
    if not isinstance(DEBUG, bool):
        raise ValueError('DEBUG must be a bool')
    if not isinstance(SECRET_KEY, str) or not SECRET_KEY:
        raise ValueError('SECRET_KEY must be a >0-length string')
except (IOError, KeyError, ValueError) as e:
    sys.stderr.write('{}: {}\n'.format(config, e))
    sys.exit(1)
