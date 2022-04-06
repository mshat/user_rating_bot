from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .models import MyUser, UserAnswer, UserQuestion
from .serializers import UserSerializer, UserQuestionSerializer, UserAnswerSerializer


class UserView(APIView):
    def get(self, request, tg_user_id: int):
        """
        Возвращает пользователя с указанным tg_user_id или возвращает 404
        """
        user = get_object_or_404(MyUser.objects.all(), tg_user_id=tg_user_id)
        serializer = UserSerializer(user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, tg_user_id: int):
        """
        Обновляет пользователя с указанным tg_user_id или возвращает 404
        """
        user = get_object_or_404(MyUser.objects.all(), tg_user_id=tg_user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            serializer_dict = serializer.data
            return Response(serializer_dict, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, tg_user_id: int):
        """
        Удаляет пользователя с указанным tg_user_id или возвращает 404
        """
        user = get_object_or_404(MyUser.objects.all(), tg_user_id=tg_user_id)
        user.delete()
        return Response(status=status.HTTP_200_OK)


class UsersListView(APIView):
    def get(self, request):
        """
        Возвращает список пользователей
        """
        users = MyUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            error_data = {'message': f'Invalid data!', 'validate errors': serializer.errors}
            return Response(status=status.HTTP_400_BAD_REQUEST, data=error_data)

        new_user = MyUser(
            tg_user_id=serializer.data["tg_user_id"], first_name=serializer.data["first_name"],
            last_name=serializer.data["last_name"], username=serializer.data["username"]
        )
        new_user.save()
        return Response(status=status.HTTP_200_OK, data={'id': new_user.id})


class UserQuestionView(APIView):
    def get(self, request, question_id: int):
        """
        Возвращает вопрос c указанным id или возвращает 404
        """
        question = get_object_or_404(UserQuestion.objects.all(), id=question_id)
        serializer = UserQuestionSerializer(question)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, question_id: int):
        """
        Обновляет вопрос с указанным id или возвращает 404
        """
        pass

    def delete(self, request, question_id: int):
        """
        Удаляет вопрос с указанным id или возвращает 404
        """
        question = get_object_or_404(UserQuestion.objects.all(), id=question_id)
        question.delete()
        return Response(status=status.HTTP_200_OK)


class UserQuestionsListView(APIView):
    def get(self, request):
        """
        Возвращает список ответов пользователя
        """
        if 'user-id' not in request.headers:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': "Header 'user-id' not found"})

        user_id = request.headers['user-id']
        questions = UserQuestion.objects.filter(user_id=user_id)
        serializer = UserQuestionSerializer(questions, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request):
        serializer = UserQuestionSerializer(data=request.data)
        if not serializer.is_valid():
            error_data = {'message': f'Invalid data!', 'validate errors': serializer.errors}
            return Response(status=status.HTTP_400_BAD_REQUEST, data=error_data)

        user = get_object_or_404(MyUser.objects.all(), id=serializer.data["user_id"])
        new_question = UserQuestion(user_id=user, question=serializer.data["question"])
        if "likes_num" in serializer.data:
            new_question.likes_num = serializer.data["likes_num"]
        if "dislikes_num" in serializer.data:
            new_question.dislikes_num = serializer.data["dislikes_num"]
        if "has_an_answer" in serializer.data:
            new_question.has_an_answer = serializer.data["has_an_answer"]

        new_question.save()
        return Response(status=status.HTTP_200_OK, data={'id': new_question.id})


class UserAnswerView(APIView):
    def get(self, request, answer_id: int):
        """
        Возвращает ответ c указанным id или возвращает 404
        """
        answer = get_object_or_404(UserAnswer.objects.all(), id=answer_id)
        serializer = UserAnswerSerializer(answer)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, answer_id: int):
        """
        Обновляет вответ с указанным id или возвращает 404
        """
        pass

    def delete(self, request, answer_id: int):
        """
        Удаляет ответ с указанным id или возвращает 404
        """
        answer = get_object_or_404(UserAnswer.objects.all(), id=answer_id)
        answer.delete()
        return Response(status=status.HTTP_200_OK)


class UserAnswersListView(APIView):
    def get(self, request):
        """
        Возвращает список вопросов пользователя
        """
        if 'user-id' not in request.headers:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': "Header 'user-id' not found"})

        user_id = request.headers['user-id']
        questions = UserAnswer.objects.filter(user_id=user_id)
        serializer = UserAnswerSerializer(questions, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request):
        serializer = UserAnswerSerializer(data=request.data)
        if not serializer.is_valid():
            error_data = {'message': f'Invalid data!', 'validate errors': serializer.errors}
            return Response(status=status.HTTP_400_BAD_REQUEST, data=error_data)

        user = get_object_or_404(MyUser.objects.all(), id=serializer.data["user_id"])
        new_answer = UserAnswer(user_id=user, answer=serializer.data["answer"])
        if "likes_num" in serializer.data:
            new_answer.likes_num = serializer.data["likes_num"]
        if "dislikes_num" in serializer.data:
            new_answer.dislikes_num = serializer.data["dislikes_num"]
        if "best_answer" in serializer.data:
            new_answer.has_an_answer = serializer.data["best_answer"]

        new_answer.save()
        return Response(status=status.HTTP_200_OK, data={'id': new_answer.id})

