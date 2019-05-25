from django.core.validators import validate_email
from django.core import exceptions
from django.contrib.auth.models import User

from rest_framework import serializers


class EmailValidator:
    """
    Custom email validator. Validate that email is valid and
    depending on user_should_exists check is users exists or not.
    """
    def __init__(self, user_should_exists: bool):
        self.user_should_exists = user_should_exists

    def __call__(self, value: str):
        errors = dict()
        try:
            validate_email(value)
        except exceptions.ValidationError as e:
            errors['email'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        if not self.user_should_exists and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        elif self.user_should_exists and not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exists.")