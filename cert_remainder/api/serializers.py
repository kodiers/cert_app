from rest_framework import serializers

from common.serializers import IdFieldMixin
from people.api.serializers import UserSerializer
from certifications.api.serializers import CertificationSerializer, ExamSerializer
from cert_remainder.models import UserCertification, UserExam


class UserCertificationSerializer(serializers.ModelSerializer, IdFieldMixin):
    """
    User certification serializer
    """
    user = UserSerializer()
    certification = CertificationSerializer()

    class Meta:
        model = UserCertification
        fields = '__all__'


class UserExamSerializer(serializers.ModelSerializer, IdFieldMixin):
    """
    User exam serializer
    """
    user = UserSerializer()
    user_certification = UserCertificationSerializer()
    exam = ExamSerializer()

    class Meta:
        model = UserExam
        fields = '__all__'
