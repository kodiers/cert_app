from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from certifications.models import Vendor, Certification, Exam

from .serializers import VendorSerializer, CertificationSerializer, ExamSerializer, AddCertificationToExamSerializer


class VendorListAPIView(ListAPIView):
    """
    Vendor list api view
    """
    permission_classes = (IsAuthenticated,)
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorRetrieveAPIView(RetrieveAPIView):
    """
    Retrieve vendor by id
    """
    permission_classes = (IsAuthenticated,)
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class CertificationListCreateAPIView(ListCreateAPIView):
    """
    Certification list create api view
    """
    permission_classes = (IsAuthenticated,)
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('vendor',)
    parser_classes = (JSONParser, MultiPartParser, FormParser)


class CertificationRetrieveAPIView(RetrieveAPIView):
    """
    Retrieve certification by id
    """
    permission_classes = (IsAuthenticated,)
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer


class ExamListCreateAPIView(ListCreateAPIView):
    """
    Exam list create api view
    """
    permission_classes = (IsAuthenticated,)
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('certification', 'certification__vendor')


class ExamRetrieveAPIView(RetrieveAPIView):
    """
    Retrieve exam by id
    """
    permission_classes = (IsAuthenticated,)
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer


class AddCertificationToExamUpdateAPIView(UpdateAPIView):
    """
    Add certification to exam update view
    """
    permission_classes = (IsAuthenticated,)
    queryset = Exam.objects.all()
    http_method_names = ['put']
    serializer_class = AddCertificationToExamSerializer

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Exam, pk=kwargs['pk'])
        serializer = AddCertificationToExamSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.refresh_from_db()
        return Response(ExamSerializer(instance).data, status=status.HTTP_200_OK)
