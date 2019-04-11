from django.test import TestCase

from certifications.api.serializers import (
    VendorSerializer,
    CertificationSerializer,
    ExamSerializer,
    AddCertificationToExamSerializer
)
from certifications.tests.recipes import vendor_recipe, certification_recipe, exam_with_certification, exam_recipe


class TestVendorSerializer(TestCase):
    """
    Simple test for vendor serializer
    """
    def test_fields(self):
        vendor = vendor_recipe.make()
        serializer = VendorSerializer(instance=vendor)
        data = serializer.data
        self.assertEqual(data['id'], vendor.id)
        self.assertEqual(data['title'], vendor.title)
        self.assertEqual(data['description'], vendor.description)


class TestCertificationSerializer(TestCase):
    """
    Simple test for CertificationSerializer
    """
    def test_fields(self):
        certification = certification_recipe.make()
        serializer = CertificationSerializer(instance=certification)
        data = serializer.data
        self.assertEqual(data['id'], certification.id)
        self.assertEqual(data['title'], certification.title)
        self.assertEqual(data['description'], certification.description)
        self.assertEqual(data['number'], certification.number)
        self.assertEqual(data['vendor'], certification.vendor.pk)


class TestExamSerializer(TestCase):
    """
    Simple test for ExamSerializer
    """
    def test_fields(self):
        exam = exam_with_certification.make()
        serializer = ExamSerializer(instance=exam)
        data = serializer.data
        self.assertEqual(data['id'], exam.id)
        self.assertEqual(data['title'], exam.title)
        self.assertEqual(data['description'], exam.description)
        self.assertEqual(data['number'], exam.number)
        self.assertTrue(exam.certification.all()[0].pk in data['certification'])


class TestAddCertificationToExamSerializer(TestCase):
    """
    Test AddCertificationToExamSerializer
    """
    def test_updata(self):
        exam = exam_recipe.make()
        certification = certification_recipe.make()
        serializer = AddCertificationToExamSerializer()
        data = {'certification': [certification]}
        updated_exam = serializer.update(exam, data)
        self.assertTrue(certification in updated_exam.certification.all())
