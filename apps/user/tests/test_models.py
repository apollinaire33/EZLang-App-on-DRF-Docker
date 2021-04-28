import pytest
from django.test import TestCase
from rest_framework.test import APIClient


pytestmark = pytest.mark.django_db

class TestUserAccountModel(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        self.User = get_user_model()
        
        self.client = APIClient()

        self.register_url = 'http://localhost:8000/api/v1/user/signup/'

    def test_email_missed_or_already_exists(self):
        user_data = {
            'name': 'vasya_voron',
            'password': 123456
        }

        response = self.client.post(self.register_url, data=user_data)

        assert response.json()['email'][0] == 'This field is required.'
        assert response.status_code == 400

        user_data = {
            'name': 'vasya_voron',
            'email': 'test@mail.ru',
            'password': 123456
        }

        response = self.client.post(self.register_url, data=user_data)

        response_error = self.client.post(self.register_url, data=user_data)

        assert response_error.json()['email'][0] == 'user account with this email already exists.'
        assert response_error.status_code == 400

    def test_password_missed_or_too_short(self):
        user_data = {
            'name': 'vasya_voron',
            'email': 'test@mail.ru',
        }

        response = self.client.post(self.register_url, data=user_data)

        assert response.json()['password'][0] == 'This field is required.'
        assert response.status_code == 400

        user_data = {
            'name': 'vasya_voron',
            'email': 'test@mail.ru',
            'password': 1,
        }

        response = self.client.post(self.register_url, data=user_data)

        assert response.json()['error'] == 'Password must be at least 6 characters'
        assert response.status_code == 400

    def test_user_str(self):
        our_user = self.User.objects.create_user(email='test@mail.ru', 
                                                 password='1234', 
                                                 name='qwerty')   

        assert str(our_user) == 'test@mail.ru'

    def test_create_super_user_func(self):
        our_user = self.User.objects.create_superuser(email='test@mail.ru',
                                                      password='1234', 
                                                      name='qwerty')   
        
        assert our_user.is_superuser == True 
        assert our_user.is_staff == True 



