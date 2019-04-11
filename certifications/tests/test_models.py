from unittest.mock import Mock

from django.test import TestCase
from django.core.files import File

from certifications.tests.recipes import vendor_recipe, certification_recipe, exam_with_certification


class TestVendor(TestCase):
    """
    Test vendor model methods
    """
    @classmethod
    def setUpTestData(cls):
        cls.vendor = vendor_recipe.make()

    def test_str(self):
        self.assertEqual(str(self.vendor), self.vendor.title)

    def test_image_tag(self):
        mock_image = Mock(spec=File)
        mock_image.name = 'test'
        self.vendor.image = mock_image
        self.assertTrue('img' in self.vendor.image_tag())


class TestCertification(TestCase):
    """
    Test certification model methods
    """
    @classmethod
    def setUpTestData(cls):
        cls.certification = certification_recipe.make()

    def test_str(self):
        self.assertEqual(str(self.certification), self.certification.title)

    def test_image_tag(self):
        mock_image = Mock(spec=File)
        mock_image.name = 'test'
        self.certification.image = mock_image
        self.assertTrue('img' in self.certification.image_tag())


class TestExam(TestCase):
    """
    Test exam model methods
    """
    def setUp(self) -> None:
        self.exam = exam_with_certification.make()

    def test_str(self):
        self.assertEqual(str(self.exam), self.exam.title)

    def test_exam_full_title(self):
        self.assertEqual(self.exam.exam_full_title, "{} {}".format(self.exam.number, self.exam.title))

    def test_exam_full_title_without_number(self):
        self.exam.number = None
        self.exam.save()
        self.assertEqual(self.exam.exam_full_title, self.exam.title)
