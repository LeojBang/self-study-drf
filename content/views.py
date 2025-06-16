from rest_framework import viewsets

from authentication.permissions import IsAdmin, IsOwner, IsTeacher

from .models import Course, Material, Section
from .serializers import (CourseSerializer, MaterialSerializer,
                          SectionSerializer)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdmin | (IsTeacher & IsOwner)]
        elif self.action == "create":
            self.permission_classes = [IsAdmin | IsTeacher]

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role == "teacher":
            return Course.objects.filter(owner=user)
        return super().get_queryset()


class SectionViewSet(viewsets.ModelViewSet):
    serializer_class = SectionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "teacher":
            return Section.objects.filter(course__owner=user)
        return Section.objects.all()

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdmin | (IsTeacher & IsOwner)]

        return super().get_permissions()


class MaterialViewSet(viewsets.ModelViewSet):
    serializer_class = MaterialSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "teacher":
            return Material.objects.filter(section__course__owner=user)

        return Material.objects.all()

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdmin | (IsTeacher & IsOwner)]

        return super().get_permissions()
