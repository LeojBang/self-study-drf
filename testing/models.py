from django.conf import settings
from django.db import models

from content.models import Material

User = settings.AUTH_USER_MODEL


class Test(models.Model):
    material = models.OneToOneField(
        Material, on_delete=models.CASCADE, related_name="test"
    )
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"Тест: {self.title}"


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'верный' if self.is_correct else 'неверный'})"


class TestAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()
    passed = models.BooleanField()
    submitted_at = models.DateTimeField(auto_now_add=True)
