from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

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
    filter_fields = ('user_certification__certification', 'date_of_pass', 'remind_at_date')

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
