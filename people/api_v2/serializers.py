from django.contrib.auth.models import User

from rest_framework import serializers

from people.models import PasswordResetToken
from people.api.serializers import UserRegistrationSerializer
from people.api_v2.validators import EmailValidator, PasswordValidator


class UserRegistrationSerializerV2(UserRegistrationSerializer):
    """
    User registration serializer
    """
    email = serializers.EmailField(min_length=8, max_length=50, validators=[EmailValidator(user_should_exists=False)])

    def create(self, validated_data: dict) -> User:
        """
        Create user
        """
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')
        instance = User.objects.create_user(username=username, password=password, email=email)
        return instance


class RequestPasswordResetSerializer(serializers.Serializer):
    """
    Request password reset token
    """
    email = serializers.EmailField(min_length=8, max_length=50, validators=[EmailValidator(user_should_exists=True)])

    def validate(self, attrs: dict) -> dict:
        email = attrs.get('email')
        user = User.objects.get(email=email)
        if not user.is_active:
            raise serializers.ValidationError("User with this email is not active.")
        return attrs

    def create(self, validated_data: dict):
        """
        Create password reset token
        """
        email = validated_data.get('email')
        instance = PasswordResetToken.create_password_reset_token(email)
        return instance


class ResetPasswordSerializer(serializers.Serializer):
    """
    Password reset serializer
    """
    token = serializers.CharField(max_length=64)
    password = serializers.CharField(min_length=8, max_length=50, validators=[PasswordValidator()])
    confirm_password = serializers.CharField(min_length=8, max_length=50)

    def validate_token(self, value):
        try:
            token = PasswordResetToken.objects.get(token=value)
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("Token incorrect.")
        if token.expired:
            raise serializers.ValidationError("Token is expired.")
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        token = attrs.get('token')
        if password != confirm_password:
            raise serializers.ValidationError(_("Password and confirm password don't match"))
        try:
            user = User.objects.get(reset_token__token=token)
        except User.DoesNotExist:
            raise serializers.ValidationError("Token incorrect.")
        if not user.is_active:
            raise serializers.ValidationError("User is not active.")
        return attrs
