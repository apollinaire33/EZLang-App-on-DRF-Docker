from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError

from homework.enums import HomeworkStatus

User = get_user_model()


# Service class for counting marks for specific user
class UserMark:
    # func for counting average mark of homeworks
    def common_hw_mark(user_id):
        from homework.models import Homework
        user_homework_list = Homework.objects.filter(user=user_id)
        mark_list = [i.mark for i in user_homework_list if
                     i.status == HomeworkStatus.FINISHED or i.status == HomeworkStatus.FAILED]
        if mark_list:
            result = sum(mark_list) / len(mark_list)
            User.objects.filter(id=user_id).update(mark_hw=round(result, 2))
        elif not mark_list:
            content = {
                "error": "Wow! You somehow managed to create and delete so fast! Take an Error as a reward."
            }
            raise ValidationError(content, code=status.HTTP_400_BAD_REQUEST)

    # func for counting average mark of quizes
    def common_quiz_mark(user_id):
        from quiz.models import QuizTaker
        user_quiz_list = QuizTaker.objects.filter(user=user_id)
        mark_list = [i.score for i in user_quiz_list
                     if i.status == HomeworkStatus.FINISHED or i.status == HomeworkStatus.FAILED]
        if mark_list:
            result = sum(mark_list) / len(mark_list)
            User.objects.filter(id=user_id).update(mark_tests=round(result, 2))
        elif not mark_list:
            content = {
                "error": "Wow! You somehow managed to create and delete so fast! Take an Error as a reward."
            }
            raise ValidationError(content, code=status.HTTP_400_BAD_REQUEST)


# Service class for verification of Homework objects about to process
class HomeworkObjectVerification:
    # Func for verification if current user is the owner of requested homework
    def catching_a_sneak(self, request, error):
        instance = self.get_object()
        if instance.user.id != request.user.id and request.user.is_superuser is False:
            content = {
                "error": error
            }
            raise ValidationError(content, code=status.HTTP_400_BAD_REQUEST)

    # Func for verification if current user is the owner of requested homework list
    def catching_a_list_sneak(self, request, error):
        instance_list = self.get_queryset()
        if instance_list:
            instance = instance_list[0]
            if instance.user.id != request.user.id and request.user.is_superuser is False:
                content = {
                    "error": error
                }
                raise ValidationError(content, code=status.HTTP_400_BAD_REQUEST)
