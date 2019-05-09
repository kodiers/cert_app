from settings.base import *
from settings.local import default_db, celery_broker_url, celery_result_backend, email_settings


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

# EMAIL BACKEND
EMAIL_BACKEND = email_settings['email_backend']
EMAIL_HOST_USER = email_settings['email_host_user']
FAIL_EMAIL_SILENTLY = email_settings['email_fail_silently']
EMAIL_USE_TLS = email_settings['email_use_tls']
EMAIL_HOST = email_settings['email_host']
EMAIL_PORT = email_settings['email_port']
EMAIL_HOST_PASSWORD = email_settings['email_host_password']
