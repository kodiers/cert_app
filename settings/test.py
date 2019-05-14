from settings.base import *


DEBUG = True
DEVELOP = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}


MEDIA_URL = '/media/'

STATIC_ROOT = (os.path.join(BASE_DIR, 'static'))

CORS_ORIGIN_WHITELIST = (
    'localhost:8000',
    '127.0.0.1:8000',
    'localhost:4200',
    '127.0.0.1:4200',
)

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# EMAIL BACKEND
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
EMAIL_HOST_USER = 'test@test.ru'
FAIL_EMAIL_SILENTLY = False
