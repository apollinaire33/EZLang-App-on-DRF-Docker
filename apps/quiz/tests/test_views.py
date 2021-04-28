import datetime

import pytest
from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from user.models import UserAccount
from quiz.models import Quiz, Question, Answer, QuizTaker


pytestmark = pytest.mark.django_db

class TestAuth(TestCase):
    def setUp(self):
        self.client = APIClient()

        # method 1
        # from rest_framework.authtoken.models import Token
        # from django.contrib.auth import get_user_model
        # User = get_user_model()

        # self.our_user = User.objects.create(email='test@mail.ru', password='1234')        

        # self.token = Token.objects.create(user=self.our_user)

        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # method 2
        from django.contrib.auth import get_user_model
        User = get_user_model()

        self.our_user = User.objects.create_superuser(email='test@mail.ru', password='1234', name='qwerty')   

        self.token_url = 'http://localhost:8000/api/token/'

        user_data = {
            'email': 'test@mail.ru',
            'password': 1234
        }

        response = self.client.post(self.token_url, data=user_data)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])


class TestQuizFilterViewSet(TestAuth):
    def test_quiz_filter_list_works(self):
        # create homework
        quiz_tasked = mixer.blend(Quiz, date_expiry='9999-04-08T12:24:17Z')
        quiz_tasked1 = mixer.blend(Quiz, date_expiry='4555-04-08T12:24:17Z')
        quiz_taker_tasked = mixer.blend(QuizTaker, quiz=quiz_tasked, user=self.our_user, status='Tasked')
        
        quiz_tasked_and_failed = mixer.blend(Quiz)
        quiz_taker_tasked_and_failed = mixer.blend(QuizTaker, quiz=quiz_tasked_and_failed, user=self.our_user, status='Tasked')
        
        url_tasked = reverse('apiv1:tasked')
        response_tasked = self.client.get(url_tasked)
        
        assert response_tasked.json() != None
        assert len(response_tasked.json()) == 1
        assert response_tasked.status_code == 200


        quiz_finished = mixer.blend(Quiz)
        quiz_taker_finished = mixer.blend(QuizTaker, quiz=quiz_finished, user=self.our_user, status='Tasked')
        QuizTaker.objects.filter(id=quiz_taker_finished.id).update(score=54, status='Finished')
        quiz_taker_finished.refresh_from_db()
        url_finished = reverse('apiv1:finished')
        response_finished = self.client.get(url_finished)


        assert response_finished.json() != None
        assert len(response_finished.json()) == 1
        assert response_finished.status_code == 200 
        

        quiz_failed = mixer.blend(Quiz)
        quiz_taker_failed = mixer.blend(QuizTaker, quiz=quiz_failed, user=self.our_user, status='Tasked')
        QuizTaker.objects.filter(id=quiz_taker_failed.id).update(score=0, status='Failed')
        quiz_taker_failed.refresh_from_db()
        url_failed = reverse('apiv1:failed')
        response_failed = self.client.get(url_failed)

        assert response_failed.json() != None
        assert len(response_failed.json()) == 2
        assert response_failed.status_code == 200 


class TestUserAnswerViewset(TestAuth):
    def test_user_answer_create_method(self):
        self.user = mixer.blend(UserAccount)

        self.quiz = mixer.blend(Quiz)
        self.question = mixer.blend(Question, quiz=self.quiz, question='poggers?')
        self.answer = mixer.blend(Answer, question=self.question, text='true lulw')

        self.quiz_taker_wrong = mixer.blend(QuizTaker, quiz=self.quiz, user=self.user)

        self.quiz_taker = mixer.blend(QuizTaker, quiz=self.quiz, user=self.our_user)

        url = reverse('apiv1:useranswer-list')
        
        input_data_wrong = {
            'quiz_taker': self.quiz_taker_wrong.pk,
            'question': self.question.pk,
            'answer': self.answer.pk
        }

        response_wrong = self.client.post(url, data=input_data_wrong)

        input_data_correct = {
            'quiz_taker': self.quiz_taker.pk,
            'question': self.question.pk,
            'answer': self.answer.pk
        }

        response_correct = self.client.post(url, data=input_data_correct)
        
        assert response_wrong.json()['error'] == 'You are not the owner of quiztaker!'
        assert response_correct.json() != None


class TestQuizTakerViewSet(TestAuth):
    def test_quiz_taker_create_error_method(self):
        self.quiz_missed = mixer.blend(Quiz, date_expiry='1234-04-08T12:24:17Z')
       
        self.quiz_completed = mixer.blend(Quiz, date_expiry='6793-04-08T12:24:17Z')
        self.quiz_taker_completed = mixer.blend(QuizTaker, quiz=self.quiz_completed, user=self.our_user)

        url = reverse('apiv1:quiztaker-list')
        
        input_data_missed = {
            'user': self.our_user.pk, 
            'quiz': self.quiz_missed.pk, 
            'score': 0, 
            'status': 'Failed', 
            'date_finished': datetime.datetime.now(), 
            'date_started': datetime.datetime.now()
        }

        response_missed = self.client.post(url, data=input_data_missed)

        input_data_completed = {
            'user': self.our_user.pk, 
            'quiz': self.quiz_completed.pk, 
            'score': 0, 
            'status': 'Finished', 
            'date_finished': datetime.datetime.now(), 
            'date_started': datetime.datetime.now()
        }

        response_completed = self.client.post(url, data=input_data_completed)
        
        assert response_missed.json()['error'] == 'You missed this quiz!'
        assert response_completed.json()['error'] == 'You already completed this quiz!'

    def test_quiz_taker_create_method(self):
        quiz_new = mixer.blend(Quiz, date_expiry='2222-04-08T12:24:17Z')

        url = reverse('apiv1:quiztaker-list')
        input_data = {
            'user': self.our_user.pk, 
            'quiz': quiz_new.pk,
            'score': 0,
            'status': 'Tasked', 
            'date_finished': datetime.datetime.now(), 
            'date_started': datetime.datetime.now()
        }

        response = self.client.post(url, data=input_data)

        assert response.json() != None
        assert response.status_code == 201