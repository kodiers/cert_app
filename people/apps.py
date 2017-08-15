from django.apps import AppConfig


class PeopleConfig(AppConfig):
    name = 'people'

    def ready(self):
        from .signals import create_profile_and_token
