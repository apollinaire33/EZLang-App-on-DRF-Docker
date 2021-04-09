import pytest
from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from user.models import UserAccount


pytestmark = pytest.mark.django_db

class TestUserViewSet(TestCase):

    def setUp(self):
        self.client = APIClient()

        from django.contrib.auth import get_user_model
        User = get_user_model()

        self.our_user = User.objects.create_user(email='test@mail.ru', password='1234', name='qwerty')   

        self.token_url = 'http://localhost:8000/api/token/'

        user_data = {
            'name': 'vasya_voron',
            'email': 'test@mail.ru',
            'password': 1234
        }

        response = self.client.post(self.token_url, data=user_data)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

    def test_user_list_works(self):
        # create homework
        url = reverse('user-list-list')

        # call the url
        response = self.client.get(url)
        
        # assertion
        assert response.json() != None
        assert len(response.json()) == 1
        assert response.status_code == 200

    def test_user_detail_works(self):
        url = reverse('user-list-detail', kwargs={'pk': self.our_user.pk})
        response = self.client.get(url)

        assert response.json() != None
        assert response.status_code == 200

    def test_user_delete_error(self):
        another_user = mixer.blend(UserAccount)
        url = reverse('user-list-detail', kwargs={'pk': another_user.pk})
        response = self.client.delete(url)

        assert response.json()['error'] == "Stop fooling around with other people's accounts! Shame on you!"
        assert response.status_code == 400
        
        url = reverse('user-list-detail', kwargs={'pk': self.our_user.pk})
        response = self.client.delete(url)
        assert response.status_code == 204

    def test_user_update_works(self):
        another_user = mixer.blend(UserAccount)

        input_data = {
            'name': 'kavo_and_sho',
            'email': 'test@mail.ru',
            'password': 1234
        }

        url = reverse('user-list-detail', kwargs={'pk': another_user.pk})
        response = self.client.put(url, data=input_data)

        assert response.json()['error'] == "Stop fooling around with other people's accounts! Shame on you!"
        assert response.status_code == 400

        url = reverse('user-list-detail', kwargs={'pk': self.our_user.pk})
        response = self.client.put(url, data=input_data)

        assert response.status_code == 200

