from django.test import TestCase
from django.utils import timezone

from people.tests.recipes import user_recipe
from certifications.tests.recipes import exam_with_certification

from cert_remainder.models import UserCertification, UserExam
from cert_remainder.tests.recipes import user_certification_recipe, user_exam_recipe


class TestUserCertification(TestCase):
    """
    Test UserCertification methods
    """
    @classmethod
    def setUpTestData(cls):
        cls.user_cert = user_certification_recipe.make()

    def test_str(self):
        self.assertEqual(str(self.user_cert),  "{} {}".format(self.user_cert.user.username,
                                                              self.user_cert.certification.title))


class TestUserExam(TestCase):
    """
    Test UserExam
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = user_recipe.make()
        cls.exam = exam_with_certification.make()
        user_cert = UserCertification.objects.create(user=cls.user, certification=cls.exam.certification.all()[0],
                                                     expiration_date=timezone.now())
        cls.user_exam = UserExam.objects.create(user=cls.user, user_certification=user_cert, exam=cls.exam,
                                                date_of_pass=timezone.now())

    def test_str(self):
        self.assertEqual(str(self.user_exam), "{} {}".format(self.user_exam.user.username, self.user_exam.exam.title))