from content.apps import ContentConfig
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from content.views import CourseViewSet, SectionViewSet, MaterialViewSet

app_name = ContentConfig.name


router = SimpleRouter()
router.register('courses', CourseViewSet, basename='courses')
router.register('sections', SectionViewSet, basename='sections')
router.register('materials', MaterialViewSet, basename='materials')

urlpatterns = [
    path('', include(router.urls)),
]