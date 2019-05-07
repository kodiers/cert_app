from django.contrib.auth.models import User

from rest_framework import serializers

from people.api.serializers import UserRegistrationSerializer


class UserRegistrationSerializerV2(UserRegistrationSerializer):
    """
    User registration serializer
    """
    email = serializers.EmailField(min_length=8, max_length=50)

    def create(self, validated_data: dict):
        """
        Create user
        """
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')
        instance = User.objects.create_user(username=username, password=password, email=email)
        return instance
