from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import User
from content.models import Course, Material, Section

from .serializers import (CourseSerializer, MaterialSerializer,
                          SectionSerializer)


class ModelTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            email="teacher@example.com", password="testpass", role="teacher"
        )

        self.student = User.objects.create_user(
            email="student@example.com", password="studentpass", role="student"
        )
        self.admin = User.objects.create_superuser(
            email="admin@example.com", password="adminpass"
        )

        self.course = Course.objects.create(title="Test Course", owner=self.teacher)
        self.section = Section.objects.create(title="Test Section", course=self.course)
        self.material = Material.objects.create(
            title="Test Material", content="Test Content", section=self.section
        )

        # Создаем чужой курс, секцию и материал
        self.other_teacher = User.objects.create_user(
            email="other_teacher@example.com", password="testpass", role="teacher"
        )
        self.other_course = Course.objects.create(
            title="Other Course", owner=self.other_teacher
        )
        self.other_section = Section.objects.create(
            title="Other Section", course=self.other_course
        )

    def test_course_creation(self):
        self.assertEqual(str(self.course), "Test Course")
        self.assertEqual(self.course.owner, self.teacher)

    def test_section_creation(self):
        self.assertEqual(str(self.section), "Test Course — Test Section")

    def test_material_creation(self):
        self.assertEqual(str(self.material), "Test Section — Test Material")

    def test_course_serializer(self):
        serializer = CourseSerializer(self.course)
        self.assertEqual(serializer.data["title"], "Test Course")
        self.assertEqual(serializer.data["owner"], self.teacher.id)

    def test_section_serializer(self):
        serializer = SectionSerializer(self.section)
        self.assertEqual(serializer.data["title"], "Test Section")
        self.assertEqual(serializer.data["course"], self.course.id)

    def test_material_serializer(self):
        serializer = MaterialSerializer(self.material)
        self.assertEqual(serializer.data["title"], "Test Material")
        self.assertEqual(serializer.data["section"], self.section.id)

    # Тесты для CourseViewSet
    def test_list_courses(self):
        url = reverse("content:courses-list")
        self.client.force_authenticate(user=self.student)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course_as_teacher(self):
        url = reverse("content:courses-list")
        data = {"title": "New Course", "description": "New Desc"}
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 3)

    def test_update_course_as_owner(self):
        url = reverse("content:courses-detail", args=[self.course.id])
        data = {"title": "Updated Title"}
        self.client.force_authenticate(user=self.teacher)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Updated Title")

    # Тесты для SectionViewSet
    def test_create_section_as_teacher(self):
        url = reverse("content:sections-list")
        data = {"title": "New Section", "course": self.course.id}
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_teacher_sees_only_own_section(self):
        Section.objects.create(title="Other Section", course=self.other_course)
        # Аутентифицируемся как основной teacher
        self.client.force_authenticate(user=self.teacher)
        url = reverse("content:sections-list")
        response = self.client.get(url)

        # Проверяем, что в ответе только своя секция
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data]
        self.assertIn("Test Section", titles)
        self.assertNotIn("Other Section", titles)

    # Тесты для MaterialViewSet
    def test_create_material_as_teacher(self):
        url = reverse("content:materials-list")
        data = {
            "title": "New Material",
            "content": "New Content",
            "section": self.section.id,
        }
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_teacher_sees_only_own_materials(self):
        Material.objects.create(
            title="Other Material", content="Other Content", section=self.other_section
        )
        # Аутентифицируемся как основной teacher
        self.client.force_authenticate(user=self.teacher)
        url = reverse("content:materials-list")
        response = self.client.get(url)

        # Проверяем, что в ответе только свой материал
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data]
        self.assertIn("Test Material", titles)
        self.assertNotIn("Other Material", titles)
