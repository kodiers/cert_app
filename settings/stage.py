from settings.base import *
from settings.local import allowed_hosts, default_db, cors_list, celery_broker_url, celery_result_backend


DEBUG = True
DEVELOP = False

ALLOWED_HOSTS = allowed_hosts

DATABASES = {
    'default': default_db
}


MEDIA_URL = '/media/'

STATIC_ROOT = (os.path.join(BASE_DIR, 'static'))

CORS_ORIGIN_WHITELIST = cors_list

CELERY_BROKER_URL = celery_broker_url
CELERY_RESULT_BACKEND = celery_result_backend
