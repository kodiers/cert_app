from django.test import TestCase
from django.urls import reverse

from people.tests.recipes import user_recipe

from certifications.models import Vendor, Certification, Exam
from certifications.tests.recipes import vendor_recipe, certification_recipe, exam_with_certification, exam_recipe


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


class TestCertificationListCreateAPIView(TestCase):
    """
    Test CertificationListCreateAPIView
    """
    @classmethod
    def setUpTestData(cls):
        cls.password = 'p@ssw0rd11'
        cls.user = user_recipe.make()
        cls.user.set_password(cls.password)
        cls.user.save()
        cls.certification = certification_recipe.make()
        cls.url = reverse('api:certifications_api:certifications')

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
        self.assertEqual(data['count'], Certification.objects.count())
        certification_data = data['results'][0]
        self.assertEqual(certification_data['id'], self.certification.id)
        self.assertEqual(certification_data['title'], self.certification.title)
        self.assertEqual(certification_data['description'], self.certification.description)
        self.assertEqual(certification_data['number'], self.certification.number)
        self.assertEqual(certification_data['vendor'], self.certification.vendor.pk)

    def test_post(self):
        data = {"title": "testCreate", "number": "testCreate_1", "image": '', "description": "testCreate",
                "deprecated": False, "vendor": self.certification.vendor.pk}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        certification_data = response.data
        for key, value in data.items():
            if key != 'image':
                self.assertEqual(certification_data[key], value)
        self.assertEqual(Certification.objects.count(), 2)


class TestCertificationRetrieveAPIView(TestCase):
    """
    Test CertificationRetrieveAPIView
    """
    @classmethod
    def setUpTestData(cls):
        cls.password = 'p@ssw0rd11'
        cls.user = user_recipe.make()
        cls.user.set_password(cls.password)
        cls.user.save()
        cls.certification = certification_recipe.make()
        cls.url = reverse('api:certifications_api:certification', args=[cls.certification.pk])

    def setUp(self) -> None:
        self.client.login(username=self.user.username, password=self.password)

    def test_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        certification_data = response.data
        self.assertEqual(certification_data['id'], self.certification.id)
        self.assertEqual(certification_data['title'], self.certification.title)
        self.assertEqual(certification_data['description'], self.certification.description)
        self.assertEqual(certification_data['number'], self.certification.number)
        self.assertEqual(certification_data['vendor'], self.certification.vendor.pk)


class TestExamListCreateAPIView(TestCase):
    """
    Test ExamListCreateAPIView
    """
    @classmethod
    def setUpTestData(cls):
        cls.password = 'p@ssw0rd11'
        cls.user = user_recipe.make()
        cls.user.set_password(cls.password)
        cls.user.save()
        cls.exam = exam_with_certification.make()
        cls.url = reverse('api:certifications_api:exams')

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
        self.assertEqual(data['count'], Exam.objects.count())
        exam_data = data['results'][0]
        self.assertEqual(exam_data['id'], self.exam.id)
        self.assertEqual(exam_data['title'], self.exam.title)
        self.assertEqual(exam_data['description'], self.exam.description)
        self.assertEqual(exam_data['number'], self.exam.number)
        self.assertTrue(self.exam.certification.all()[0].pk in exam_data['certification'])

    def test_post(self):
        data = {"title": "testCreate", "number": "testCreate_1", "description": "testCreate",
                "deprecated": False, "certification": [self.exam.certification.all()[0].pk]}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        exam_data = response.data
        for key, value in data.items():
            if key != 'image':
                self.assertEqual(exam_data[key], value)
        self.assertEqual(Exam.objects.count(), 2)


class TestExamRetrieveAPIView(TestCase):
    """
    Test ExamRetrieveAPIView
    """
    @classmethod
    def setUpTestData(cls):
        cls.password = 'p@ssw0rd11'
        cls.user = user_recipe.make()
        cls.user.set_password(cls.password)
        cls.user.save()
        cls.exam = exam_with_certification.make()
        cls.url = reverse('api:certifications_api:exam', args=[cls.exam.pk])

    def setUp(self) -> None:
        self.client.login(username=self.user.username, password=self.password)

    def test_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        exam_data = response.data
        self.assertEqual(exam_data['id'], self.exam.id)
        self.assertEqual(exam_data['title'], self.exam.title)
        self.assertEqual(exam_data['description'], self.exam.description)
        self.assertEqual(exam_data['number'], self.exam.number)
        self.assertTrue(self.exam.certification.all()[0].pk in exam_data['certification'])


class TestAddCertificationToExamUpdateAPIView(TestCase):
    """
    Test AddCertificationToExamUpdateAPIView
    """

    @classmethod
    def setUpTestData(cls):
        cls.password = 'p@ssw0rd11'
        cls.user = user_recipe.make()
        cls.user.set_password(cls.password)
        cls.user.save()
        cls.exam = exam_recipe.make()
        cls.url = reverse('api:certifications_api:add_cert_to_exam', args=[cls.exam.pk])

    def setUp(self) -> None:
        self.client.login(username=self.user.username, password=self.password)

    def test_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_patch(self):
        new_certification = certification_recipe.make()
        response = self.client.patch(self.url, {"certification": [new_certification.pk]},
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)
        exam_data = response.data
        self.assertEqual(exam_data['id'], self.exam.id)
        self.assertEqual(exam_data['title'], self.exam.title)
        self.assertEqual(exam_data['description'], self.exam.description)
        self.assertEqual(exam_data['number'], self.exam.number)
        self.assertTrue(new_certification.pk in exam_data['certification'])
