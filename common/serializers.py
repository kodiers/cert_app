from rest_framework import serializers


class IdFieldMixin:
    id = serializers.ReadOnlyField()
