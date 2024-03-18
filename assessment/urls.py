from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import views

app_name = 'assessment'

urlpatterns = [
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs', SpectacularSwaggerView.as_view(url_name='assessment:schema'), name='docs'),
    path('students',
         views.StudentsViewSet.as_view(
             {'post': 'create', 'get': 'list'}
         ), name='students'),
    path('students/<str:id>',
         views.StudentsViewSet.as_view(
             {'get': 'retrieve', 'delete': 'destroy'}
         ), name='student-detail'),
    path('works', views.WorksViewSet.as_view({'post': 'create'}), name='works'),
    path('works/request', views.WorksViewSet.as_view({'get': 'request_works'}), name='request-works'),
    path('works/status', views.WorksViewSet.as_view({'get': 'list'}), name='works-status'),
    path('works/<str:id>', views.WorksViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='work-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
