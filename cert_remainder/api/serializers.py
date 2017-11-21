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
        user_cert = UserCertification(user=user, certification=certification, expiration_date=expiration_date,
                                      remind_at_date=remind_at_date)
        user_cert.save()
        return user_cert

    def update(self, instance, validated_data):
        certification = validated_data.pop('certification_id')
        expiration_date = validated_data.pop('expiration_date')
        remind_at_date = validated_data.pop('remind_at_date')
        instance.certification = certification
        instance.expiration_date = expiration_date
        instance.remind_at_date = remind_at_date
        instance.save()
        return instance

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

    def create(self, validated_data):
        user = self.context['request'].user
        user_certification = validated_data.pop('user_certification_id')
        exam = validated_data.pop('exam_id')
        date_of_pass = validated_data.pop('date_of_pass')
        remind_at_date = validated_data.pop('remind_at_date')
        user_exam = UserExam(user=user, user_certification=user_certification, exam=exam, date_of_pass=date_of_pass,
                             remind_at_date=remind_at_date)
        user_exam.save()
        return user_exam

    def update(self, instance, validated_data):
        user_certification = validated_data.pop('user_certification_id')
        exam = validated_data.pop('exam_id')
        date_of_pass = validated_data.pop('date_of_pass')
        remind_at_date = validated_data.pop('remind_at_date')
        instance.user_certification = user_certification
        instance.exam = exam
        instance.date_of_pass = date_of_pass
        instance.remind_at_date = remind_at_date
        instance.save()
        return instance

    class Meta:
        model = UserExam
        fields = '__all__'


class BulkUserExamSerializer(serializers.Serializer):
    """
    Serializer for bulk create user exams
    """
    exams = serializers.ListField(child=UserExamSerializer(), min_length=1, max_length=20)

    def create(self, validated_data):
        user = self.context['request'].user
        exams_data_list = validated_data.get('exams')
        created_exams = list()
        for exam_data in exams_data_list:
            instance = UserExam(user=user, user_certification=exam_data['user_certification_id'],
                                exam=exam_data['exam_id'], date_of_pass=exam_data['date_of_pass'],
                                remind_at_date=exam_data['remind_at_date'])
            instance.save()
            created_exams.append(instance)
        return {'exams': created_exams}
