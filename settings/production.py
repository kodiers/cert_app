from settings.base import *
from settings.local import (
    allowed_hosts,
    default_db,
    cors_list,
    celery_broker_url,
    celery_result_backend,
    email_settings,
    frontend_password_reset_url,
    chrome_driver_path
)


DEBUG = False
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

# EMAIL BACKEND
EMAIL_BACKEND = email_settings['email_backend']
EMAIL_HOST_USER = email_settings['email_host_user']
FAIL_EMAIL_SILENTLY = email_settings['email_fail_silently']
EMAIL_USE_TLS = email_settings['email_use_tls']
EMAIL_HOST = email_settings['email_host']
EMAIL_PORT = email_settings['email_port']
EMAIL_HOST_PASSWORD = email_settings['email_host_password']

FRONTEND_PASSWORD_RESET_URL = frontend_password_reset_url

CHROME_WEBDRIVER_PATH = chrome_driver_path
