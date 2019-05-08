from settings.base import *
from settings.local import default_db, celery_broker_url, celery_result_backend


DEBUG = True
DEVELOP = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': default_db
}


MEDIA_URL = '/media/'

STATIC_ROOT = (os.path.join(BASE_DIR, 'static'))

CORS_ORIGIN_WHITELIST = (
    'localhost:8000',
    '127.0.0.1:8000',
    'localhost:4200',
    '127.0.0.1:4200',
)

CELERY_BROKER_URL = celery_broker_url
CELERY_RESULT_BACKEND = celery_result_backend
