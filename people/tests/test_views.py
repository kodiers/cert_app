from django.test import TestCase
from django.urls import reverse

from people.tests.recipes import user_recipe


class TestUserRegistrationAPIView(TestCase):
    """
    Test UserRegistrationAPIView
    """
    def test_post(self):
        username = "test"
        password = "p@ssw0rd11"
        data = {"username": username, 'password': password, 'confirm_password': password}
        response = self.client.post(reverse('api:people_api:registration'), data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["user"]["username"], username)
        self.assertIsNotNone(response.data["token"])


class TestGetUserInfoAPIView(TestCase):
    """
    Test GetUserInfoAPIView
    """
    @classmethod
    def setUpTestData(cls):
        cls.password = "p@ssw0rd11"
        cls.user = user_recipe.make()
        cls.user.set_password(cls.password)
        cls.user.save()
        cls.url = reverse('api:people_api:user')

    def setUp(self) -> None:
        self.client.login(username=self.user.username, password=self.password)

    def test_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["user"]["username"], self.user.username)
        self.assertTrue(response.data["user"]["first_name"], self.user.first_name)
        self.assertTrue(response.data["user"]["last_name"], self.user.last_name)
        self.assertTrue(response.data["country"], self.user.profile.country)
        self.assertIsNotNone(response.data["token"])
