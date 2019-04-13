from unittest.mock import Mock
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from model_mommy import mommy

from people.tests.recipes import user_recipe
from certifications.models import Certification
from certifications.tests.recipes import certification_recipe

from cert_remainder.api.serializers import UserCertificationSerializer
from cert_remainder.tests.recipes import user_certification_recipe


class TestUserCertificationSerializer(TestCase):
    """
    Test UserCertificationSerializer
    """
    @classmethod
    def setUpTestData(cls):
        cls.now = timezone.now()
        cls.user = user_recipe.make()
        cls.serializer = UserCertificationSerializer()
        mock_request = Mock()
        mock_request.user = cls.user
        cls.serializer.context['request'] = mock_request

    def test_create(self):
        certification = certification_recipe.make()
        data = {'certification_id': certification, 'expiration_date': self.now, 'remind_at_date': None}
        user_certification = self.serializer.create(data)
        self.assertEqual(user_certification.user, self.user)
        self.assertEqual(user_certification.certification, certification)
        self.assertEqual(user_certification.expiration_date, self.now)

    def test_update(self):
        now_plus_hour = self.now + timedelta(hours=1)
        user_certification = user_certification_recipe.make(user=self.user)
        new_certification = mommy.make(Certification)
        data = {'certification_id': new_certification, 'expiration_date': now_plus_hour, 'remind_at_date': None}
        _ = self.serializer.update(user_certification, data)
        user_certification.refresh_from_db()
        self.assertEqual(user_certification.user, self.user)
        self.assertEqual(user_certification.certification, new_certification)
        self.assertEqual(user_certification.expiration_date, now_plus_hour.date())

