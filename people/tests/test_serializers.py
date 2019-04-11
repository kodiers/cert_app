from django.test import TestCase

from rest_framework.serializers import ValidationError

from people.serializers import UserRegistrationSerializer, UserSerializer, ProfileSerializer

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

    def test_validate_password_success(self):
        password = self.serializer.validate_password(self.password)
        self.assertEqual(password, self.password)

    def test_validate_password_empty(self):
        with self.assertRaisesMessage(ValidationError, "Password are required"):
            self.serializer.validate_password('')

    def test_validate_password_simple(self):
        self.assertRaises(ValidationError, self.serializer.validate_password, 'password')

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
