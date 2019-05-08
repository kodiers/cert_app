default_db = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': '',
}

allowed_hosts = []

cors_list = (
    'localhost:8000',
)

celery_broker_url = 'redis://localhost:6379/0'
celery_result_backend = 'redis://localhost:6379/0'