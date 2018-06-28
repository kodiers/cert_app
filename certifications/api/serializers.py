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


class AddCertificationToExamSerializer(serializers.ModelSerializer):
    """
    Add certification to exam serializer
    """
    certification = serializers.PrimaryKeyRelatedField(queryset=Certification.objects.all(), many=True)

    def update(self, instance, validated_data):
        certification = validated_data.get('certification')
        instance.certification.add(*certification)
        return instance

    class Meta:
        model = Exam
        fields = ('certification',)
