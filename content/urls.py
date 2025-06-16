from django.urls import include, path
from rest_framework.routers import SimpleRouter

from content.apps import ContentConfig
from content.views import CourseViewSet, MaterialViewSet, SectionViewSet

app_name = ContentConfig.name


router = SimpleRouter()
router.register("courses", CourseViewSet, basename="courses")
router.register("sections", SectionViewSet, basename="sections")
router.register("materials", MaterialViewSet, basename="materials")

urlpatterns = [
    path("", include(router.urls)),
]
