from settings.base import *
from settings.local import allowed_hosts, default_db, cors_list


DEBUG = True
DEVELOP = False

ALLOWED_HOSTS = allowed_hosts

DATABASES = {
    'default': default_db
}


MEDIA_URL = '/media/'

STATIC_ROOT = (os.path.join(BASE_DIR, 'static'))

CORS_ORIGIN_WHITELIST = cors_list
