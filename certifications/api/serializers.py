from rest_framework import serializers

from common.serializers import IdFieldMixin
from certifications.models import Vendor, Certification, Exam


class VendorSerializer(serializers.ModelSerializer, IdFieldMixin):
    """
    Vendor model serializer
    """
    class Meta:
        fields = '__all__'
        model = Vendor


class CertificationSerializer(serializers.ModelSerializer, IdFieldMixin):
    """
    Certification model serializer
    """
    class Meta:
        fields = '__all__'
        model = Certification


class ExamSerializer(serializers.ModelSerializer, IdFieldMixin):
    """
    Exam model serializer
    """
    class Meta:
        fields = '__all__'
        model = Exam
