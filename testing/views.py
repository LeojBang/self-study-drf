from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Answer, Test, TestAttempt
from .serializers import SubmitTestSerializer, TestSerializer


class TestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class SubmitTestView(APIView):

    @swagger_auto_schema(request_body=SubmitTestSerializer)
    def post(self, request, test_id):
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
        passed = score >= 70  # можно вынести в настройки

        TestAttempt.objects.create(
            user=request.user, test=test, score=score, passed=passed
        )

        return Response({"score": score, "passed": passed}, status=status.HTTP_200_OK)
