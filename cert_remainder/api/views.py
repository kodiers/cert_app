from django.shortcuts import get_object_or_404

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from cert_remainder.models import UserCertification, UserExam

from .serializers import UserCertificationSerializer, UserExamSerializer, BulkUserExamSerializer
from .mixins import CreateMixin


class UserCertificationListCreateAPIView(ListCreateAPIView, CreateMixin):
    """
    User certification list create api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserCertificationSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('certification', 'expiration_date', 'remind_at_date')

    def get_queryset(self):
        queryset = UserCertification.objects.filter(user=self.request.user)
        return queryset


class UserCertificationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Get user certification api view by id
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserCertificationSerializer

    def get_queryset(self):
        queryset = UserCertification.objects.filter(user=self.request.user)
        return queryset


class UserExamListCreateAPIView(ListCreateAPIView, CreateMixin):
    """
    User exams list create api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserExamSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user_certification', 'user_certification__certification', 'date_of_pass', 'remind_at_date')

    def get_queryset(self):
        queryset = UserExam.objects.filter(user=self.request.user)
        return queryset


class UserExamRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Get user exams api view by id
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserExamSerializer

    def get_queryset(self):
        queryset = UserExam.objects.filter(user=self.request.user)
        return queryset


class BulkUserExamCreateAPIView(CreateAPIView, CreateMixin):
    """
    Bulk create user exams API view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BulkUserExamSerializer


class BulkUserExamUpdateAPIView(UpdateAPIView):
    """
    Bulk update user exams API view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BulkUserExamSerializer

    def update(self, request, *args, **kwargs):
        exams_data = request.data.get('exams')
        updated_exams = list()
        for exam_data in exams_data:
            exam = get_object_or_404(UserExam, pk=exam_data.get('id'))
            if exam.user != request.user:
                return Response({'Error': 'You cannot update this exam'}, status=status.HTTP_403_FORBIDDEN)
            serializer = UserExamSerializer(instance=exam, data=exam_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            updated_exams.append(serializer.data)
        return Response({'exams': updated_exams}, status=status.HTTP_200_OK)
