from django.urls import path
from rest_framework import routers

from quiz.views import (QuizViewSet, QuizFilterViewSet, 
                        QuestionViewSet, AnswerViewSet, 
                        QuizTakerViewSet, UserAnswerViewSet)


router = routers.DefaultRouter()

router.register(r'quizes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'quiz_takers', QuizTakerViewSet)
router.register(r'user_answers', UserAnswerViewSet)

# Urls for filtering
urlpatterns = [
    path('filter/tasked/', QuizFilterViewSet.as_view({'get': 'list_tasked'}), name='tasked'),
    path('filter/finished/', QuizFilterViewSet.as_view({'get': 'list_finished'}), name='finished'),
    path('filter/failed/', QuizFilterViewSet.as_view({'get': 'list_failed'}), name='failed'),
]

urlpatterns += router.urls
