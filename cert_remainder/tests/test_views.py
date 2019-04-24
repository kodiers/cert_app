from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from certifications.models import Vendor
from people.tests.recipes import user_recipe
from certifications.tests.recipes import certification_recipe

from cert_remainder.tests.recipes import user_certification_recipe


class TestUserCertificationListCreateAPIView(TestCase):
    """
    Test UserCertificationListCreateAPIView
    """
    @classmethod
    def setUpTestData(cls):
        cls.now = timezone.now()
        cls.password = 'p@ssw0rd11'
        cls.user = user_recipe.make()
        cls.user.set_password(cls.password)
        cls.user.save()
        cls.user_certification = user_certification_recipe.make(user=cls.user)
        cls.url = reverse('api:cert_remainder_api:user_certifications')

    def setUp(self) -> None:
        self.client.login(username=self.user.username, password=self.password)

    def test_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        user_cert_data = response.data['results'][0]
        self.assertEqual(user_cert_data['id'], self.user_certification.id)
        self.assertEqual(user_cert_data['user']['id'], self.user.id)
        self.assertEqual(user_cert_data['certification_id'], self.user_certification.certification.id)
        self.assertEqual(datetime.strptime(user_cert_data['expiration_date'], '%Y-%m-%d').date(),
                         self.user_certification.expiration_date)

    def test_post(self):
        new_certification = certification_recipe.make(title='Test-1', number='test-1', vendor=Vendor.objects.all()[0])
        data = {"certification_id": new_certification.pk, "expiration_date": self.now.strftime('%Y-%m-%d'),
                'remind_at_date': None}
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        user_cert_data = response.data
        self.assertEqual(user_cert_data['user']['id'], self.user.id)
        self.assertEqual(user_cert_data['certification_id'], new_certification.id)
        self.assertEqual(datetime.strptime(user_cert_data['expiration_date'], '%Y-%m-%d').date(), self.now.date())
        self.assertIsNone(user_cert_data['remind_at_date'])


class TestUserCertificationRetrieveUpdateDestroyAPIView(TestCase):
    """
    Test UserCertificationRetrieveUpdateDestroyAPIView
    """
    @classmethod
    def setUpTestData(cls):
        cls.now = timezone.now()
        cls.password = 'p@ssw0rd11'
        cls.user = user_recipe.make()
        cls.user.set_password(cls.password)
        cls.user.save()

    def setUp(self) -> None:
        self.user_certification = user_certification_recipe.make(user=self.user)
        self.url = reverse('api:cert_remainder_api:user_certification', args=[self.user_certification.pk])
        self.client.login(username=self.user.username, password=self.password)

    def test_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        user_cert_data = response.data
        self.assertEqual(user_cert_data['id'], self.user_certification.id)
        self.assertEqual(user_cert_data['user']['id'], self.user.id)
        self.assertEqual(user_cert_data['certification_id'], self.user_certification.certification.id)
        self.assertEqual(datetime.strptime(user_cert_data['expiration_date'], '%Y-%m-%d').date(),
                         self.user_certification.expiration_date)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)