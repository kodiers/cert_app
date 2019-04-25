from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from certifications.models import Vendor
from people.tests.recipes import user_recipe
from certifications.tests.recipes import certification_recipe, exam_with_certification, exam_recipe

from cert_remainder.models import UserExam
from cert_remainder.tests.recipes import user_certification_recipe, user_exam_recipe


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
        data = {'certification_id': new_certification.pk, 'expiration_date': self.now.strftime('%Y-%m-%d'),
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

    def test_update(self):
        new_expiration_date = self.now + timedelta(days=10)
        data = {'expiration_date': new_expiration_date.strftime('%Y-%m-%d'),
                'certification_id': self.user_certification.certification.pk, 'remind_at_date': None}
        response = self.client.patch(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        user_cert_data = response.data
        self.assertEqual(datetime.strptime(user_cert_data['expiration_date'], '%Y-%m-%d').date(),
                         new_expiration_date.date())


class TestUserExamListCreateAPIView(TestCase):
    """
    Test UserExamListCreateAPIView
    """
    @classmethod
    def setUpTestData(cls):
        cls.now = timezone.now()
        cls.password = 'p@ssw0rd11'
        cls.user = user_recipe.make()
        cls.user.set_password(cls.password)
        cls.user.save()
        cls.exam = exam_with_certification.make()
        cls.user_certification = user_certification_recipe.make(user=cls.user,
                                                                certification=cls.exam.certification.all()[0])
        cls.user_exam = user_exam_recipe.make(user=cls.user, user_certification=cls.user_certification, exam=cls.exam)
        cls.url = reverse('api:cert_remainder_api:user_exams')

    def setUp(self) -> None:
        self.client.login(username=self.user.username, password=self.password)

    def test_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        user_exam_data = response.data['results'][0]
        self.assertEqual(user_exam_data['id'], self.user_certification.id)
        self.assertEqual(user_exam_data['user']['id'], self.user.id)
        self.assertEqual(user_exam_data['user_certification_id'], self.user_certification.id)
        self.assertEqual(user_exam_data['exam_id'], self.user_exam.exam.pk)
        self.assertEqual(datetime.strptime(user_exam_data['date_of_pass'], '%Y-%m-%d').date(),
                         self.user_certification.expiration_date)

    def test_create(self):
        new_exam = exam_recipe.make(title='Test-1', number='test-1')
        new_exam.certification.add(self.user_certification.certification)
        data = {'user_certification_id': self.user_certification.pk, 'exam_id': new_exam.pk,
                'date_of_pass': self.now.strftime('%Y-%m-%d'), 'remind_at_date': None}
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        user_exam_data = response.data
        self.assertEqual(user_exam_data['user']['id'], self.user.id)
        self.assertEqual(user_exam_data['user_certification_id'], self.user_certification.id)
        self.assertEqual(user_exam_data['exam_id'], new_exam.pk)
        self.assertEqual(datetime.strptime(user_exam_data['date_of_pass'], '%Y-%m-%d').date(),
                         self.now.date())


class TestUserExamRetrieveUpdateDestroyAPIView(TestCase):
    """
    Test UserExamRetrieveUpdateDestroyAPIView
    """
    @classmethod
    def setUpTestData(cls):
        cls.now = timezone.now()
        cls.password = 'p@ssw0rd11'
        cls.user = user_recipe.make()
        cls.user.set_password(cls.password)
        cls.user.save()
        cls.exam = exam_with_certification.make()
        cls.user_certification = user_certification_recipe.make(user=cls.user,
                                                                certification=cls.exam.certification.all()[0])

    def setUp(self) -> None:
        self.user_exam = user_exam_recipe.make(user=self.user, user_certification=self.user_certification,
                                               exam=self.exam)
        self.url = reverse('api:cert_remainder_api:user_exam', args=[self.user_exam.pk])
        self.client.login(username=self.user.username, password=self.password)

    def test_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        user_exam_data = response.data
        self.assertEqual(user_exam_data['id'], self.user_certification.id)
        self.assertEqual(user_exam_data['user']['id'], self.user.id)
        self.assertEqual(user_exam_data['user_certification_id'], self.user_certification.id)
        self.assertEqual(user_exam_data['exam_id'], self.user_exam.exam.pk)
        self.assertEqual(datetime.strptime(user_exam_data['date_of_pass'], '%Y-%m-%d').date(),
                         self.user_certification.expiration_date)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(UserExam.objects.filter(pk=self.user_exam.pk).exists())

    def test_update(self):
        new_date_of_pass = self.now + timedelta(days=100)
        data = {'user_certification_id': self.user_certification.pk, 'exam_id': self.exam.pk,
                'date_of_pass': new_date_of_pass.strftime('%Y-%m-%d'), 'remind_at_date': self.now.strftime('%Y-%m-%d')}
        response = self.client.patch(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        user_exam_data = response.data
        self.assertEqual(user_exam_data['id'], self.user_certification.id)
        self.assertEqual(user_exam_data['user']['id'], self.user.id)
        self.assertEqual(user_exam_data['user_certification_id'], self.user_certification.id)
        self.assertEqual(user_exam_data['exam_id'], self.user_exam.exam.pk)
        self.assertEqual(datetime.strptime(user_exam_data['date_of_pass'], '%Y-%m-%d').date(), new_date_of_pass.date())
        self.assertEqual(datetime.strptime(user_exam_data['remind_at_date'], '%Y-%m-%d').date(), self.now.date())


class TestBulkUserExamCreateAPIView(TestCase):
    """
    Test BulkUserExamCreateAPIView
    """
    @classmethod
    def setUpTestData(cls):
        cls.now = timezone.now()
        cls.password = 'p@ssw0rd11'
        cls.user = user_recipe.make()
        cls.user.set_password(cls.password)
        cls.user.save()
        cls.exam = exam_with_certification.make()
        cls.user_certification = user_certification_recipe.make(user=cls.user,
                                                                certification=cls.exam.certification.all()[0])
        cls.url = reverse('api:cert_remainder_api:bulk_create_user_exams')

    def setUp(self) -> None:
        self.client.login(username=self.user.username, password=self.password)

    def test_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_create(self):
        data = {'exams': [{'exam_id': self.exam.pk, 'user_certification_id': self.user_certification.pk,
                           'date_of_pass': self.now.strftime('%Y-%m-%d'), 'remind_at_date': None}]}
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        user_exam_data = response.data['exams'][0]
        self.assertEqual(user_exam_data['user']['id'], self.user.id)
        self.assertEqual(user_exam_data['user_certification_id'], self.user_certification.id)
        self.assertEqual(user_exam_data['exam_id'], self.exam.pk)
        self.assertEqual(datetime.strptime(user_exam_data['date_of_pass'], '%Y-%m-%d').date(), self.now.date())
        self.assertIsNone(user_exam_data['remind_at_date'])


class TestBulkUserExamUpdateAPIView(TestCase):
    """
    Test BulkUserExamUpdateAPIView
    """
    @classmethod
    def setUpTestData(cls):
        cls.now = timezone.now()
        cls.password = 'p@ssw0rd11'
        cls.user = user_recipe.make()
        cls.user.set_password(cls.password)
        cls.user.save()
        cls.exam = exam_with_certification.make()
        cls.user_certification = user_certification_recipe.make(user=cls.user,
                                                                certification=cls.exam.certification.all()[0])
        cls.user_exam = user_exam_recipe.make(user=cls.user, user_certification=cls.user_certification, exam=cls.exam)
        cls.url = reverse('api:cert_remainder_api:bulk_update_user_exams')

    def setUp(self) -> None:
        self.client.login(username=self.user.username, password=self.password)

    def test_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_update(self):
        new_date_of_pass = self.now + timedelta(days=100)
        data = {'exams': [{'id': self.user_exam.pk, 'exam_id': self.exam.pk,
                           'user_certification_id': self.user_certification.pk,
                           'date_of_pass': new_date_of_pass.strftime('%Y-%m-%d'),
                           'remind_at_date': self.now.strftime('%Y-%m-%d')}]}
        response = self.client.patch(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        user_exam_data = response.data['exams'][0]
        self.assertEqual(user_exam_data['user']['id'], self.user.id)
        self.assertEqual(user_exam_data['user_certification_id'], self.user_certification.id)
        self.assertEqual(user_exam_data['exam_id'], self.exam.pk)
        self.assertEqual(datetime.strptime(user_exam_data['date_of_pass'], '%Y-%m-%d').date(), new_date_of_pass.date())
        self.assertEqual(datetime.strptime(user_exam_data['remind_at_date'], '%Y-%m-%d').date(), self.now.date())
