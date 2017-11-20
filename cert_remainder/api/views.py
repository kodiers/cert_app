from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from cert_remainder.models import UserCertification, UserExam

from .serializers import UserCertificationSerializer, UserExamSerializer
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

    def create_user_exam(self, data):
        serializer = UserExamSerializer(data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if type(data) is list:
            response_data = list()
            for d in data:
                serializer = self.create_user_exam(d)
                response_data.append(serializer.data)
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            serializer = self.create_user_exam(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserExamRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Get user exams api view by id
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserExamSerializer

    def get_queryset(self):
        queryset = UserExam.objects.filter(user=self.request.user)
        return queryset
