import datetime

import pytest
from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from homework.models import Homework
from user.models import UserAccount


pytestmark = pytest.mark.django_db

class TestHomeworkAdministratingViewSet(TestCase):

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

    def test_homework_list_works(self):
        # create homework
        homework = mixer.blend(Homework, task='just get a house lulw')
        url = reverse('for-admin-list')

        # call the url
        response = self.client.get(url)

        # assertion
        assert response.json() != None
        assert len(response.json()) == 1
        assert response.status_code == 200

    def test_homework_create_works(self):
        # data 
        user = mixer.blend(UserAccount)
        input_data = {
            'task': 'just get a house lulw',
            'mark': 0,
            'status': 'Tasked', 
            'task_load': '', 
            'desc_for_mark': '',
            'user': user.id,
            'created_at': datetime.datetime.now(),
            'date_expiry': datetime.datetime.now()
        }
        url = reverse('for-admin-list')

        # call the url
        response = self.client.post(url, data=input_data)

        # assertion
        assert response.json() != None
        assert response.status_code == 201
        assert Homework.objects.count() == 1

    def test_homework_detail_works(self):
        homework = mixer.blend(Homework, task='just get a house lulw')
        url = reverse('for-admin-detail', kwargs={'pk': homework.pk})
        response = self.client.get(url)

        # assertion
        assert response.json() != None
        assert response.status_code == 200
        assert response.json()['task'] == 'just get a house lulw'

    def test_homework_delete_works(self):
        homework = mixer.blend(Homework, task='just get a house lulw')
        url = reverse('for-admin-detail', kwargs={'pk': homework.pk})
        response = self.client.delete(url)

        # assertion
        assert Homework.objects.count() == 0
        assert response.status_code == 204

    def test_homework_update_works(self):
        user = mixer.blend(UserAccount)
        homework = mixer.blend(Homework, task='just get a house lulw', user=None)
        assert homework.user == None

        input_data = {
            'task': 'just get a house lulw',
            'mark': 0,
            'status': 'Tasked', 
            'task_load': '', 
            'desc_for_mark': '',
            'user': user.pk,
            'created_at': datetime.datetime.now(),
            'date_expiry': datetime.datetime.now()
        }

        url = reverse('for-admin-detail', kwargs={'pk': homework.pk})
        response = self.client.put(url, data=input_data)
        # assertion
        assert response.status_code == 200
        assert Homework.objects.count() == 1
        assert Homework.objects.last().user == user


class TestHomeworkViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()

        from django.contrib.auth import get_user_model
        User = get_user_model()

        self.our_user = User.objects.create_user(email='test@mail.ru', password='1234', name='qwerty')   

        self.token_url = 'http://localhost:8000/api/token/'

        user_data = {
            'email': 'test@mail.ru',
            'password': 1234
        }

        response = self.client.post(self.token_url, data=user_data)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

    def test_homework_list_for_user_works(self):
        # wrong user
        another_user = mixer.blend(UserAccount)

        homework = mixer.blend(Homework, task='just get a house lulw', user=another_user)
        url = reverse('homework_list_for_user-list')

        response = self.client.get(url)
        # assertion
        assert response.json()['error'] == "Stop fooling around with other people's homework list! Shame on you!"
        assert response.status_code == 400

        # correct user
        Homework.objects.filter(id=homework.id).update(user=self.our_user)
        homework.refresh_from_db()
        homework.save()

        response = self.client.get(url)
        # assertion
        assert response.json() != None
        assert response.status_code == 200


class TestHomeworkTaskViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()

        from django.contrib.auth import get_user_model
        User = get_user_model()

        self.our_user = User.objects.create_user(email='test@mail.ru', password='1234', name='qwerty')   

        self.token_url = 'http://localhost:8000/api/token/'

        user_data = {
            'email': 'test@mail.ru',
            'password': 1234
        }

        response = self.client.post(self.token_url, data=user_data)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

    def test_homework_retrieve_and_update_for_user_works(self):
        # wrong user
        another_user = mixer.blend(UserAccount)

        homework = mixer.blend(Homework, task='just get a house lulw', user=another_user)
        url = reverse('homework-task-loading-detail', kwargs={'pk': homework.pk})

        response = self.client.get(url)

        assert response.json()['error'] == "Stop fooling around with other people's homework! Shame on you!"
        assert response.status_code == 400

        # updating
        input_data = {
            'task_load': '', 
            'user': another_user.pk,
        }

        url = reverse('homework-task-loading-detail', kwargs={'pk': homework.pk})
        response = self.client.put(url, data=input_data)
        
        assert response.json()['error'] == "Stop fooling around with other people's homework! Shame on you!"
        assert response.status_code == 400

        # correct user
        Homework.objects.filter(id=homework.id).update(user=self.our_user)
        homework.refresh_from_db()
        homework.save()

        response = self.client.get(url)

        assert response.json() != None
        assert response.status_code == 200  

        # updating
        input_data = {
            'task_load': '', 
            'user': another_user.pk,
        }

        url = reverse('homework-task-loading-detail', kwargs={'pk': homework.pk})
        response = self.client.put(url, data=input_data)
        
        assert response.json() != None
        assert response.status_code == 200 