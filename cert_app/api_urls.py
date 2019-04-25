from django.conf.urls import url, include


app_name = 'api'

urlpatterns = (
    url(r'^people/', include('people.urls', namespace='people_api')),
    url(r'^certifications/', include('certifications.api.urls', namespace='certifications_api')),
    url(r'^remainder/', include('cert_remainder.api.urls', namespace='cert_remainder_api'))
)
