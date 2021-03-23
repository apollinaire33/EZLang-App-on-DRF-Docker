import datetime

from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import ValidationError

from quiz.serializers import (QuizUserSerializer, QuizAdminSerializer, 
                            QuestionSerializer, AnswerSerializer, 
                            QuizTakerSerializer, UserAnswerSerializer)
from quiz.models import Quiz, Question, Answer, QuizTaker, UserAnswer
from quiz.services import FilterList


# Viewset for quiz controlling for admin only
class QuizViewSet(viewsets.mixins.RetrieveModelMixin,
                    viewsets.mixins.ListModelMixin,
                    viewsets.mixins.UpdateModelMixin,
                    viewsets.mixins.CreateModelMixin,
                    viewsets.mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizAdminSerializer
    permission_classes = (permissions.IsAdminUser, )


# Viewset for quiz filtering for certain user
class QuizFilterViewSet(viewsets.mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizUserSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def list_tasked(self, request, *args, **kwargs):
        # Checking and setting score as 0 of quiztaker if its date expired
        for i in FilterList.filtered_list(self, request, 'Tasked'):
            filtered_quiz_expiry_date = list(i.items())[3][1]
            formated_date = datetime.datetime.strptime(filtered_quiz_expiry_date, 
                                                        "%Y-%m-%dT%H:%M:%SZ")
            if formated_date < datetime.datetime.now():
                expired_quiztaker_id = list(i.items())[6][1]['id']
                QuizTaker.objects.filter(id=expired_quiztaker_id).update(status='Failed', 
                                                                        score=0)

        return Response(FilterList.filtered_list(self, request, 'Tasked'))

    def list_finished(self, request, *args, **kwargs):
        return Response(FilterList.filtered_list(self, request, 'Finished'))

    def list_failed(self, request, *args, **kwargs):
        return Response(FilterList.filtered_list(self, request, 'Failed'))


# Viewset for question controlling for admin only
class QuestionViewSet(viewsets.mixins.RetrieveModelMixin,
                    viewsets.mixins.ListModelMixin,
                    viewsets.mixins.UpdateModelMixin,
                    viewsets.mixins.CreateModelMixin,
                    viewsets.mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticated, )


# Viewset for answer controlling for admin only
class AnswerViewSet(viewsets.mixins.RetrieveModelMixin,
                    viewsets.mixins.ListModelMixin,
                    viewsets.mixins.UpdateModelMixin,
                    viewsets.mixins.CreateModelMixin,
                    viewsets.mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAdminUser, )


# Viewset for creating user answers only by authenticated 
class UserAnswerViewSet(viewsets.mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = (permissions.IsAuthenticated, )

    # Checking if requested user id equals specified quiztaker's user id 
    def create(self, request, *args, **kwargs):
        quiztaker_id = request.data['quiz_taker']
        quiztaker = get_object_or_404(QuizTaker, id=quiztaker_id)
        if request.user.id != quiztaker.user.id:
            content = {'error': 'You are not the owner of quiztaker!'}
            raise ValidationError(content, code=status.HTTP_409_CONFLICT)
        return super().create(request, *args, **kwargs)


# Viewset for quiztaker controlling for admin only
class QuizTakerViewSet(viewsets.mixins.RetrieveModelMixin,
                    viewsets.mixins.ListModelMixin,
                    viewsets.mixins.UpdateModelMixin,
                    viewsets.mixins.CreateModelMixin,
                    viewsets.mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = QuizTaker.objects.all()
    serializer_class = QuizTakerSerializer
    permission_classes = (permissions.IsAdminUser, )