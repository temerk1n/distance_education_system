from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework import routers

from . import views

app_name = 'assessment'

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'students', views.StudentsViewSet)
router.register(r'works', views.WorksViewSet)

urlpatterns = []

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
