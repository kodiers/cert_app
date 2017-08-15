from django.core import exceptions
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from common.serializers import IdFieldMixin
from people.models import Profile


class UserRegistrationSerializer(serializers.Serializer):
    """
    User registration serializer
    """
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=50)
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

    def validate_password(self, value):
        """
        Check if password match validation rules
        """
        if not value:
            raise serializers.ValidationError("Password are required")
        errors = dict()
        try:
            validate_password(password=value)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
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
        token = Token.objects.get(user=obj.user)
        return token.key

    class Meta:
        model = Profile
        fields = '__all__'
