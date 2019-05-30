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

email_settings = {
    'email_backend': 'django.core.mail.backends.console.EmailBackend',
    'email_host_user': 'test@test.ru',
    'email_fail_silently': False,
    'email_use_tls': None,
    'email_host': None,
    'email_port': None,
    'email_host_password': None
}

frontend_password_reset_url = ''
