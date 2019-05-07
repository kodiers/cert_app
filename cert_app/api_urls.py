from django.urls import path, include


app_name = 'api'

urlpatterns = (
    path('people/', include('people.api.urls', namespace='people_api')),
    path('certifications/', include('certifications.api.urls', namespace='certifications_api')),
    path('remainder/', include('cert_remainder.api.urls', namespace='cert_remainder_api')),
    path('v2', include('cert_app.api_v2_urls', namespace='api_v2'))
)
