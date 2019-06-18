from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from model_mommy import mommy
from rest_framework.exceptions import ValidationError

from people.tests.recipes import user_recipe
from certifications.models import Certification, Vendor
from certifications.tests.recipes import certification_recipe, exam_with_certification, exam_recipe

from cert_remainder.api.serializers import UserCertificationSerializer, UserExamSerializer, BulkUserExamSerializer
from cert_remainder.tests.recipes import user_certification_recipe, user_exam_recipe
from cert_remainder.tests.mocks import create_mock_request


class TestUserCertificationSerializer(TestCase):
    """
    Test UserCertificationSerializer
    """
    @classmethod
    def setUpTestData(cls):
        cls.now = timezone.now()
        cls.user = user_recipe.make()
        cls.serializer = UserCertificationSerializer()
        cls.serializer.context['request'] = create_mock_request(cls.user)

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
        self.assertEqual(user_certification.expiration_date, timezone.localtime(now_plus_hour).date())


class TestUserExamSerializer(TestCase):
    """
    Test UserExamSerializer
    """
    @classmethod
    def setUpTestData(cls):
        cls.now = timezone.now()
        cls.user = user_recipe.make()
        cls.serializer = UserExamSerializer()
        cls.serializer.context['request'] = create_mock_request(cls.user)
        cls.exam = exam_with_certification.make()
        cls.user_certification = user_certification_recipe.make(user=cls.user,
                                                                certification=cls.exam.certification.all()[0])

    def test_create(self):
        data = {'user_certification_id': self.user_certification, 'exam_id': self.exam, 'date_of_pass': self.now,
                'remind_at_date': None}
        user_exam = self.serializer.create(data)
        self.assertEqual(user_exam.user, self.user)
        self.assertEqual(user_exam.user_certification_id, self.user_certification.pk)
        self.assertEqual(user_exam.exam_id, self.exam.pk)
        self.assertEqual(user_exam.date_of_pass, self.now)
        self.assertIsNone(user_exam.remind_at_date)

    def test_update(self):
        user_exam = user_exam_recipe.make(user=self.user,
                                          user_certification=self.user_certification, exam=self.exam)
        new_certification = certification_recipe.make(title='Test-1', number='test-1', vendor=Vendor.objects.all()[0])
        new_user_certification = user_certification_recipe.make(user=self.user, certification=new_certification)
        new_exam = exam_recipe.make(title='Test-1', number='test-1')
        new_exam.certification.add(new_certification)
        data = {'user_certification_id': new_user_certification, 'exam_id': new_exam, 'date_of_pass': self.now,
                'remind_at_date': self.now}
        updated_exam = self.serializer.update(user_exam, data)
        self.assertEqual(updated_exam.user, self.user)
        self.assertEqual(updated_exam.user_certification_id, new_user_certification.pk)
        self.assertEqual(updated_exam.exam_id, new_exam.pk)
        self.assertEqual(updated_exam.date_of_pass, self.now)
        self.assertEqual(updated_exam.remind_at_date, self.now)


class TestBulkUserExamSerializer(TestCase):
    """
    Test BulkUserExamSerializer
    """
    @classmethod
    def setUpTestData(cls):
        cls.exam_1 = exam_with_certification.make()
        cls.exam_2 = exam_recipe.make(title='Test-1', number='test-1')
        cls.exam_2.certification.add(cls.exam_1.certification.all()[0])
        cls.now = timezone.now()
        cls.user = user_recipe.make()
        cls.serializer = BulkUserExamSerializer()
        cls.serializer.context['request'] = create_mock_request(cls.user)
        cls.user_certification = user_certification_recipe.make(user=cls.user,
                                                                certification=cls.exam_1.certification.all()[0])

    def test_validate_correct(self):
        data = {'exams': [{'exam_id': self.exam_1, 'user_certification_id': self.user_certification},
                          {'exam_id': self.exam_2, 'user_certification_id': self.user_certification}]}
        validated_data = self.serializer.validate(data)
        self.assertEqual(data, validated_data)

    def test_validate_incorrect(self):
        exam = exam_recipe.make(title='Test-2', number='test-2')
        data = {'exams': [{'exam_id': exam, 'user_certification_id': self.user_certification}]}
        with self.assertRaisesMessage(ValidationError, 'Exam {} is not part of certification {}'.format(
                exam.pk, self.exam_1.certification.all()[0].pk)):
            self.serializer.validate(data)

    def test_create(self):
        data = {'exams': [{'exam_id': self.exam_1, 'user_certification_id': self.user_certification,
                           'date_of_pass': self.now, 'remind_at_date': None},
                          {'exam_id': self.exam_2, 'user_certification_id': self.user_certification,
                           'date_of_pass': self.now, 'remind_at_date': None}]}
        exams_dict = self.serializer.create(data)
        self.assertEqual(len(exams_dict['exams']), 2)
        for user_exam in exams_dict['exams']:
            self.assertEqual(user_exam.user, self.user)
            self.assertEqual(user_exam.user_certification_id, self.user_certification.pk)
            self.assertIn(user_exam.exam_id, [self.exam_1.pk, self.exam_2.pk])
            self.assertEqual(user_exam.date_of_pass, self.now)
            self.assertIsNone(user_exam.remind_at_date)

    def test_update(self):
        user_exam_1 = user_exam_recipe.make(user=self.user, user_certification=self.user_certification,
                                            exam=self.exam_1)
        data = {'exams': [{'id': user_exam_1.pk, 'exam_id': self.exam_2,
                           'user_certification_id': self.user_certification, 'date_of_pass': self.now,
                           'remind_at_date': self.now}]}
        updated_user_exams = self.serializer.update([user_exam_1], data)
        for user_exam in updated_user_exams['exams']:
            self.assertEqual(user_exam.user, self.user)
            self.assertEqual(user_exam.user_certification_id, self.user_certification.pk)
            self.assertEqual(user_exam.exam_id, self.exam_2.pk)
            self.assertEqual(user_exam.date_of_pass, self.now)
            self.assertEqual(user_exam.remind_at_date, self.now)
