from django.test import TestCase

from rest_framework import serializers

from people.tests.recipes import user_recipe
from people.api_v2.validators import EmailValidator


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
            self.assertIsNone(validator(self.usr.email))

    def test_valid_email_and_should_exists(self):
        validator = EmailValidator(user_should_exists=True)
        with self.assertRaisesMessage(serializers.ValidationError, "User with this email does not exists."):
            self.assertIsNone(validator('testtest@testtest.com'))

    def test_invalid_email(self):
        validator = EmailValidator(user_should_exists=False)
        with self.assertRaisesMessage(serializers.ValidationError, "Enter a valid email address."):
            self.assertIsNone(validator('test'))