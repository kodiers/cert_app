from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from rest_framework.serializers import ValidationError

from people.models import PasswordResetToken
from people.api.serializers import UserRegistrationSerializer, UserSerializer, ProfileSerializer
from people.api_v2.serializers import (
    UserRegistrationSerializerV2,
    RequestPasswordResetSerializer,
    ResetPasswordSerializer
)

from people.tests.recipes import user_recipe


class TestUserRegistrationSerializer(TestCase):
    """
    Test UserRegistrationSerializer
    """
    @classmethod
    def setUpTestData(cls):
        cls.password = 'p@ssw0rdp@ssw0rd'
        cls.username = 'test'
        cls.serializer = UserRegistrationSerializer()

    def test_validate_success(self):
        data = {'password': self.password, 'confirm_password': self.password}
        validated_data = self.serializer.validate(data)
        self.assertEqual(validated_data, data)

    def test_validate_fail(self):
        data = {'password': self.password, 'confirm_password': 'password'}
        with self.assertRaisesMessage(ValidationError, "Password and confirm password don't match"):
            self.serializer.validate(data)

    def test_create(self):
        data = {"username": self.username, "password": self.password}
        user = self.serializer.create(data)
        self.assertEqual(user.username, self.username)


class TestUserSerializer(TestCase):
    """
    Simple test for UserSerializer
    """
    def test_fields(self):
        user = user_recipe.make()
        serializer = UserSerializer(instance=user)
        data = serializer.data
        self.assertEqual(user.id, data['id'])
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])


class TestProfileSerializer(TestCase):
    """
    Simple test for ProfileSerializer
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = user_recipe.make()
        cls.serializer = ProfileSerializer(instance=cls.user.profile)

    def test_fields(self):
        data = self.serializer.data
        self.assertEqual(self.user.id, data['user']['id'])
        self.assertEqual(self.user.username, data['user']['username'])
        self.assertEqual(self.user.email, data['user']['email'])
        self.assertEqual(self.user.first_name, data['user']['first_name'])
        self.assertEqual(self.user.last_name, data['user']['last_name'])
        self.assertEqual(self.user.profile.country, data['country'])
        self.assertEqual(self.user.profile.date_of_birth, data['date_of_birth'])
        self.assertEqual(self.user.profile.description, data['description'])
        self.assertEqual(self.user.profile.avatar, data['avatar'])

    def test_get_token(self):
        self.assertIsNotNone(self.serializer.get_token(self.user.profile))


class TestUserRegistrationSerializerV2(TestCase):
    """
    Test UserRegistrationSerializer
    """
    @classmethod
    def setUpTestData(cls):
        cls.password = 'p@ssw0rdp@ssw0rd'
        cls.username = 'test'
        cls.email = 'test@test.com'
        cls.serializer = UserRegistrationSerializerV2()

    def test_validate_success(self):
        data = {'password': self.password, 'confirm_password': self.password, 'email': self.email}
        validated_data = self.serializer.validate(data)
        self.assertEqual(validated_data, data)

    def test_validate_fail(self):
        data = {'password': self.password, 'confirm_password': 'password', 'email': self.email}
        with self.assertRaisesMessage(ValidationError, "Password and confirm password don't match"):
            self.serializer.validate(data)

    def test_create(self):
        data = {"username": self.username, "password": self.password, 'email': self.email}
        user = self.serializer.create(data)
        self.assertEqual(user.username, self.username)


class TestRequestPasswordResetSerializer(TestCase):
    """
    Test RequestPasswordResetSerializer
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = user_recipe.make()
        cls.serializer = RequestPasswordResetSerializer()

    def setUp(self) -> None:
        self.user.is_active = True
        self.user.save()

    def test_validate_valid(self):
        data = {'email': self.user.email}
        self.assertEqual(self.serializer.validate(data), data)

    def test_validate_user_not_active(self):
        self.user.is_active = False
        self.user.save()
        data = {'email': self.user.email}
        with self.assertRaisesMessage(ValidationError, "User with this email is not active."):
            self.serializer.validate(data)

    def test_create(self):
        data = {'email': self.user.email}
        token = self.serializer.create(data)
        self.assertEqual(token.user, self.user)


class TestResetPasswordSerializer(TestCase):
    """
    Test ResetPasswordSerializer
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = user_recipe.make()
        cls.token = PasswordResetToken.create_password_reset_token(cls.user.email)
        cls.serializer = ResetPasswordSerializer()

    def setUp(self) -> None:
        self.token.expire_at = timezone.now() + timedelta(days=2)
        self.token.save()
        self.user.is_active = True
        self.user.save()

    def test_validate_token_valid(self):
        self.assertEqual(self.token.token, self.serializer.validate_token(self.token.token))

    def test_validate_token_expired(self):
        self.token.expire_at = timezone.now() - timedelta(days=2)
        self.token.save()
        with self.assertRaisesMessage(ValidationError, "Token is expired."):
            self.serializer.validate_token(self.token.token)

    def test_validate_token_invalid(self):
        with self.assertRaisesMessage(ValidationError, "Token incorrect."):
            self.serializer.validate_token('some-test-token')

    def test_validate_valid(self):
        data = {'token': self.token.token, 'password': 'p@ssw0rdP@ssw0rd', 'confirm_password': 'p@ssw0rdP@ssw0rd'}
        self.assertEqual(data, self.serializer.validate(data))

    def test_validate_passwords_not_match(self):
        data = {'token': self.token.token, 'password': 'p@ssw0rdP@ssw0rd1', 'confirm_password': 'p@ssw0rdP@ssw0rd'}
        with self.assertRaisesMessage(ValidationError, "Password and confirm password doesn't match."):
            self.serializer.validate(data)

    def test_validate_user_not_exists(self):
        data = {'token': 'some-test-token', 'password': 'p@ssw0rdP@ssw0rd', 'confirm_password': 'p@ssw0rdP@ssw0rd'}
        with self.assertRaisesMessage(ValidationError, "User with this token not found."):
            self.serializer.validate(data)

    def test_validate_user_not_active(self):
        self.user.is_active = False
        self.user.save()
        data = {'token': self.token.token, 'password': 'p@ssw0rdP@ssw0rd', 'confirm_password': 'p@ssw0rdP@ssw0rd'}
        with self.assertRaisesMessage(ValidationError, "User is not active."):
            self.serializer.validate(data)
