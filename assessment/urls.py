from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'assessment'

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'students', views.StudentsViewSet)
router.register(r'works', views.WorksViewSet)

urlpatterns = []

urlpatterns += router.urls
urlpatterns = [
    path('students',
         views.StudentsViewSet.as_view(
             {'post': 'create', 'get': 'list'}
         ), name='students'),
    path('students/<str:id>',
         views.StudentsViewSet.as_view(
             {'get': 'retrieve', 'delete': 'destroy'}
         ), name='student-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
