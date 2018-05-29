from django.conf.urls import url

from .views import (
    VendorListAPIView,
    VendorRetrieveAPIView,
    CertificationListCreateAPIView,
    CertificationRetrieveAPIView,
    ExamListCreateAPIView,
    ExamRetrieveAPIView
)


app_name = 'certifications_api'

urlpatterns = (
    url(r'^vendor/$', VendorListAPIView.as_view(), name='vendors'),
    url(r'^vendor/(?P<pk>\d+)/$', VendorRetrieveAPIView.as_view(), name='vendor'),
    url(r'^certification/$', CertificationListCreateAPIView.as_view(), name='certifications'),
    url(r'^certification/(?P<pk>\d+)/$', CertificationRetrieveAPIView.as_view(), name='certification'),
    url(r'^exam/$', ExamListCreateAPIView.as_view(), name='exams'),
    url(r'^exam/(?P<pk>\d+)/$', ExamRetrieveAPIView.as_view(), name='exam')
)
