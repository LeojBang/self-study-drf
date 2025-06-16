from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Answer, Test, TestAttempt
from .serializers import SubmitTestSerializer, TestSerializer


class TestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для работы с тестами (только чтение).

    Доступные действия:
    - list: Получить список всех тестов
    - retrieve: Получить детальную информацию о тесте (с вопросами и ответами)

    Тесты доступны только для чтения всем аутентифицированным пользователям.
    """

    queryset = Test.objects.all()
    serializer_class = TestSerializer


class SubmitTestView(APIView):
    """
    API для отправки результатов теста.

    Принимает список ответов пользователя на вопросы теста,
    вычисляет результат (процент правильных ответов) и сохраняет попытку.

    Тест считается пройденным, если набрано 70% или более правильных ответов.
    """

    @swagger_auto_schema(
        request_body=SubmitTestSerializer,
        responses={
            200: "Результат тестирования (score: процент, passed: пройден ли тест)",
            404: "Тест не найден",
            400: "Неверный формат данных",
        },
        operation_description="Отправить результаты прохождения теста",
        operation_summary="Отправка результатов теста",
    )
    def post(self, request, test_id):
        """
        Обрабатывает отправку результатов теста.

        Параметры:
        - test_id: ID теста, который проходит пользователь
        - answers: список ответов пользователя в формате {question_id, selected_answer_id}

        Возвращает:
        - score: процент правильных ответов
        - passed: true/false в зависимости от того, пройден ли тест (>=70%)
        """
        serializer = SubmitTestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        test = get_object_or_404(Test, pk=test_id)
        questions = {q.id: q for q in test.questions.all()}
        correct = 0
        total = len(questions)

        for answer_data in serializer.validated_data["answers"]:
            qid = answer_data["question_id"]
            aid = answer_data["selected_answer_id"]
            question = questions.get(qid)
            if not question:
                continue
            try:
                answer = Answer.objects.get(pk=aid, question=question)
                if answer.is_correct:
                    correct += 1
            except Answer.DoesNotExist:
                continue

        score = round((correct / total) * 100)
        passed = score >= 70

        TestAttempt.objects.create(
            user=request.user, test=test, score=score, passed=passed
        )

        return Response({"score": score, "passed": passed}, status=status.HTTP_200_OK)
