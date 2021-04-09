import pytest
from django.test import TestCase
from mixer.backend.django import mixer

from homework.models import Homework


pytestmark = pytest.mark.django_db

class TestHomeworkModel(TestCase):

    # def setUp(self):
    #     self.homework1 = Homework.objects.create(
    #         task='just get a house lulw',
    #         date_expiry=datetime.datetime.now()
    #     )

    def test_homework_can_be_created(self):

        homework = mixer.blend(Homework)

        homework_result = Homework.objects.last()

        assert homework_result.id == 1

    def test_str_return(self):

        homework = mixer.blend(Homework, task='just get a house lulw')

        assert str(homework) == 'just get a house lulw'

    def test_save_method(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        our_user = User.objects.create_user(email='test@mail.ru', password='1234', name='qwerty') 

        # If homework was Tasked
        homework = mixer.blend(Homework, status='Tasked', user=our_user)

        assert homework.save() == 'Saved without changing'
       
        # If homework was Finished or Failed
        Homework.objects.filter(id=homework.id).update(status='Finished', mark=54)

        homework.refresh_from_db()
        homework.save()
        our_user.refresh_from_db()

        assert our_user.mark_hw == 54


