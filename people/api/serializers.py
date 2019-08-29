from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from rest_framework_jwt.views import jwt_response_payload_handler

from common.serializers import IdFieldMixin
from people.models import Profile
from people.api_v2.validators import PasswordValidator


class UserRegistrationSerializer(serializers.Serializer):
    """
    User registration serializer
    """
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=50, validators=[PasswordValidator()])
    confirm_password = serializers.CharField(min_length=8, max_length=50)

    def validate(self, attrs):
        """
        Check if password and confirm_password are same
        """
        validated_data = super(UserRegistrationSerializer, self).validate(attrs)
        password = validated_data.get('password')
        confirm_password = validated_data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError(_("Password and confirm password don't match"))
        return validated_data

    def validate_username(self, value: str):
        """
        Check if user with this username already exists
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("User with this username already exists.")
        return value

    def create(self, validated_data):
        """
        Create user
        """
        username = validated_data.get('username')
        password = validated_data.get('password')
        instance = User.objects.create_user(username=username, password=password)
        return instance


class UserSerializer(serializers.ModelSerializer, IdFieldMixin):
    """
    User serializer
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class ProfileSerializer(serializers.ModelSerializer, IdFieldMixin):
    """
    Profile serializer
    """
    user = UserSerializer()
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        request = self.context['request']
        token = Token.objects.get(user=obj.user)
        jwt = jwt_response_payload_handler(token, obj.user, request)
        return jwt

    class Meta:
        model = Profile
        fields = '__all__'
