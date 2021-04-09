import pytest
from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.exceptions import ValidationError
    
from quiz.models import Quiz, Question, Answer, QuizTaker, UserAnswer
from user.models import UserAccount

pytestmark = pytest.mark.django_db

class TestModels(TestCase):
    def setUp(self):
        self.user = mixer.blend(UserAccount)

        self.quiz = mixer.blend(Quiz)
        self.question = mixer.blend(Question, quiz=self.quiz, question='poggers?')
        self.answer = mixer.blend(Answer, question=self.question, text='true lulw')

        self.quiz_wrong = mixer.blend(Quiz)
        self.question_wrong = mixer.blend(Question, quiz=self.quiz_wrong, question='poggers?')
        self.answer_wrong = mixer.blend(Answer, question=self.question_wrong, text='forcenCD')

        self.quiz_taker = mixer.blend(QuizTaker, quiz=self.quiz, user=self.user)
        self.user_answer = mixer.blend(UserAnswer, quiz_taker=self.quiz_taker, question=self.question, answer=self.answer)

    def test_str_return(self):
        assert str(self.question) == 'poggers?'
        assert str(self.answer) == 'true lulw'
        assert str(self.quiz_taker) == f'{self.user.name} {str(self.quiz.id)}'
        assert str(self.user_answer) == 'true lulw'

    def test_deny_quiztaker_instance_creating(self):

        QuizTaker.objects.filter(id=self.quiz_taker.id).update(score=54, status='Finished')
        self.quiz_taker.refresh_from_db()
        try:
            QuizTaker.objects.filter(id=self.quiz_taker.id).update(score=1337, status='Finished')
            self.quiz_taker.save()
        except Exception as error:
            assert type(error) == ValidationError

    def test_deny_user_asnwer_instance_if_wrong_question(self):
        try:
            UserAnswer.objects.filter(id=self.user_answer.id).update(question=self.question_wrong)
            self.user_answer.refresh_from_db()
            self.user_answer.save()
        except Exception as error:
            assert type(error) == ValidationError
            
    def test_deny_user_asnwer_instance_if_quiz_completed(self):
        QuizTaker.objects.filter(id=self.quiz_taker.id).update(score=54, status='Finished')
        self.quiz_taker.refresh_from_db()

        try:
            UserAnswer.objects.filter(id=self.user_answer.id).update(answer=self.answer_wrong)
            self.user_answer.save()
        except Exception as error:
            assert type(error) == ValidationError
        
        



