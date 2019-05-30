from datetime import timedelta
from unittest.mock import Mock

from django.test import TestCase
from django.core.files import File
from django.utils import timezone

from people.models import Profile, PasswordResetToken
from people.tests.recipes import user_recipe


class TestProfileModel(TestCase):
    """
    Test Profile methods
    """
    @classmethod
    def setUpTestData(cls):
        user = user_recipe.make()
        cls.profile = Profile.objects.get(user=user)

    def test_avatar_tag(self):
        mock_image = Mock(spec=File)
        mock_image.name = 'test'
        self.profile.avatar = mock_image
        self.assertTrue('img' in self.profile.avatar_tag())

    def test_full_name(self):
        self.assertEqual(self.profile.full_name, "{} {}".format(self.profile.user.first_name,
                                                                self.profile.user.last_name))

    def test_str(self):
        self.assertEqual(str(self.profile), self.profile.full_name)


class TestPasswordResetTokenModel(TestCase):
    """
    Test PasswordResetToken methods
    """
    @classmethod
    def setUpTestData(cls):
        cls.token_string = 'test'
        cls.user = user_recipe.make()
        cls.now = timezone.now()
        cls.two_day_ahead = cls.now + timedelta(days=2)

    def setUp(self) -> None:
        self.token = PasswordResetToken.objects.create(user=self.user, token=self.token_string,
                                                       expire_at=self.two_day_ahead)

    def test_str(self):
        self.assertEqual(str(self.token), f"{self.user.username} expire at {self.two_day_ahead.strftime('%d-%m-%Y')}")

    def test_set_expiration_date(self):
        self.token._set_expiration_date()
        self.assertEqual(self.token.expire_at.strftime('%d-%m-%Y'), self.two_day_ahead.strftime('%d-%m-%Y'))

    def test_expired(self):
        self.assertFalse(self.token.expired)

    def test_create_password_reset_token(self):
        new_token = PasswordResetToken.create_password_reset_token(self.user.email)
        self.assertEqual(PasswordResetToken.objects.count(), 1)
        self.assertEqual(new_token.user, self.user)
        self.assertFalse(self.token.expired)
        self.assertEqual(self.token.expire_at.strftime('%d-%m-%Y'), self.two_day_ahead.strftime('%d-%m-%Y'))
