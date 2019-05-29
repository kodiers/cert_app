from django.test import TestCase

from rest_framework import serializers

from people.tests.recipes import user_recipe
from people.api_v2.validators import EmailValidator, PasswordValidator


class TestEmailValidator(TestCase):
    """
    Test EmailValidator
    """
    @classmethod
    def setUpTestData(cls):
        cls.usr = user_recipe.make()

    def test_valid_email(self):
        validator = EmailValidator(user_should_exists=True)
        self.assertIsNone(validator(self.usr.email))

    def test_valid_email_and_should_not_exists(self):
        validator = EmailValidator(user_should_exists=False)
        with self.assertRaisesMessage(serializers.ValidationError, "User with this email already exists."):
            validator(self.usr.email)

    def test_valid_email_and_should_exists(self):
        validator = EmailValidator(user_should_exists=True)
        with self.assertRaisesMessage(serializers.ValidationError, "User with this email does not exists."):
            validator('testtest@testtest.com')

    def test_invalid_email(self):
        validator = EmailValidator(user_should_exists=False)
        with self.assertRaisesMessage(serializers.ValidationError, "Enter a valid email address."):
            validator('test')


class TestPasswordValidator(TestCase):
    """
    Test PasswordValidator
    """
    @classmethod
    def setUpTestData(cls):
        cls.validator = PasswordValidator()

    def test_valid_password(self):
        self.assertIsNone(self.validator('p@ssw0rdP@ssw0rd'))

    def test_empty_password(self):
        with self.assertRaisesMessage(serializers.ValidationError, "Password are required"):
            self.validator('')

    def test_invalid_password(self):
        with self.assertRaisesMessage(serializers.ValidationError,
                                      'This password is too short. It must contain at least 8 characters.'):
            self.validator('test')
