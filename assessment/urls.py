from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'assessment'

urlpatterns = [
    path('students', views.StudentsViewSet.as_view({'post': 'create'}), name='add_student'),
    path('works', views.WorksViewSet.as_view({'post': 'create'}), name='add_work'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)