from django.conf.urls import url

from .views import (
    UserCertificationListCreateAPIView,
    UserCertificationRetrieveUpdateDestroyAPIView,
    UserExamListCreateAPIView,
    UserExamRetrieveUpdateDestroyAPIView,
    BulkUserExamCreateAPIView
)


urlpatterns = (
    url(r'^certification/$', UserCertificationListCreateAPIView.as_view(), name='user_certifications'),
    url(r'^certification/(?P<pk>\d+)/$', UserCertificationRetrieveUpdateDestroyAPIView.as_view(),
        name='user_certification'),
    url(r'^exam/$', UserExamListCreateAPIView.as_view(), name='user_exams'),
    url(r'^exam/(?P<pk>\d+)/$', UserExamRetrieveUpdateDestroyAPIView.as_view(), name='user_exam'),
    url(r'^exam/bulk/$', BulkUserExamCreateAPIView.as_view(), name='bulk_create_user_exams')
)
