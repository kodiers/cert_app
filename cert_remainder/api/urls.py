from django.conf.urls import url

from .views import (
    UserCertificationListCreateAPIView,
    UserCertificationRetrieveUpdateDestroyAPIView,
    UserExamListCreateAPIView,
    UserExamRetrieveUpdateDestroyAPIView
)


urlpatterns = (
    url(r'^certification/$', UserCertificationListCreateAPIView.as_view(), name='user_certifications'),
    url(r'^certification/(?P<pk>\d+)/$', UserCertificationRetrieveUpdateDestroyAPIView.as_view(),
        name='user_certification'),
    url(r'^exam/$', UserExamListCreateAPIView.as_view(), name='user_exams'),
    url(r'^exam/(?P<pk>\d+)/$', UserExamRetrieveUpdateDestroyAPIView.as_view(), name='user_exam')
)
