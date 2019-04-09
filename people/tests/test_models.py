from unittest.mock import Mock

from django.test import TestCase
from django.core.files import File

from people.models import Profile
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
