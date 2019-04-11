from django.test import TestCase
from django.urls import reverse

from people.tests.recipes import user_recipe

from certifications.models import Vendor
from certifications.tests.recipes import vendor_recipe


class TestVendorListAPIView(TestCase):
    """
    Test VendorListAPIView
    """
    @classmethod
    def setUpTestData(cls):
        cls.password = 'p@ssw0rd11'
        cls.user = user_recipe.make()
        cls.user.set_password(cls.password)
        cls.user.save()
        cls.vendor = vendor_recipe.make()
        cls.url = reverse('api:certifications_api:vendors')

    def setUp(self) -> None:
        self.client.login(username=self.user.username, password=self.password)

    def test_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['count'], Vendor.objects.count())
        vendor_data = data['results'][0]
        self.assertEqual(vendor_data['id'], self.vendor.id)
        self.assertEqual(vendor_data['title'], self.vendor.title)
        self.assertEqual(vendor_data['description'], self.vendor.description)


class TestVendorRetrieveAPIView(TestCase):
    """
    Test VendorRetrieveAPIView
    """
    @classmethod
    def setUpTestData(cls):
        cls.password = 'p@ssw0rd11'
        cls.user = user_recipe.make()
        cls.user.set_password(cls.password)
        cls.user.save()
        cls.vendor = vendor_recipe.make()
        cls.url = reverse('api:certifications_api:vendor', args=[cls.vendor.pk])

    def setUp(self) -> None:
        self.client.login(username=self.user.username, password=self.password)

    def test_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        vendor_data = response.data
        self.assertEqual(vendor_data['id'], self.vendor.id)
        self.assertEqual(vendor_data['title'], self.vendor.title)
        self.assertEqual(vendor_data['description'], self.vendor.description)


