from rest_framework import serializers

from common.serializers import IdFieldMixin
from people.api.serializers import UserSerializer
from certifications.api.serializers import CertificationSerializer, ExamSerializer
from certifications.models import Certification, Exam
from cert_remainder.models import UserCertification, UserExam


class UserCertificationSerializer(serializers.ModelSerializer, IdFieldMixin):
    """
    User certification serializer
    """
    user = UserSerializer(read_only=True)
    certification = CertificationSerializer(read_only=True)
    certification_id = serializers.PrimaryKeyRelatedField(queryset=Certification.objects.all())

    def create(self, validated_data):
        user = self.context['request'].user
        certification = validated_data.pop('certification_id')
        expiration_date = validated_data.pop('expiration_date')
        remind_at_date = validated_data.pop('remind_at_date')
        user_cert = UserCertification()
        user_cert.user = user
        user_cert.certification = certification
        user_cert.expiration_date = expiration_date
        user_cert.remind_at_date = remind_at_date
        user_cert.save()
        return user_cert

    class Meta:
        model = UserCertification
        fields = '__all__'


class UserExamSerializer(serializers.ModelSerializer, IdFieldMixin):
    """
    User exam serializer
    """
    user = UserSerializer(read_only=True)
    user_certification = UserCertificationSerializer(read_only=True)
    user_certification_id = serializers.PrimaryKeyRelatedField(queryset=UserCertification.objects.all())
    exam = ExamSerializer(read_only=True)
    exam_id = serializers.PrimaryKeyRelatedField(queryset=Exam.objects.all())

    class Meta:
        model = UserExam
        fields = '__all__'
