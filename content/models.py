from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return self.title


class Section(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="sections"
    )

    def __str__(self):
        return f"{self.course.title} — {self.title}"


class Material(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="materials"
    )

    def __str__(self):
        return f"{self.section.title} — {self.title}"
