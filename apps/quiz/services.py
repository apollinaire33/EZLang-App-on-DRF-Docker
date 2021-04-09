from rest_framework import status
from rest_framework.exceptions import ValidationError


# Service class for filtering lists
class FilterList:
    # Service func for filtering list by requested user id
    def filtered_list(self, request, status):
        from quiz.models import Quiz, QuizTaker
        queryset = Quiz.objects.filter(quiztaker__user=request.user.id)            

        serializer = self.get_serializer(queryset, many=True)
        
        
        filtered_quiz_list = [i for i in serializer.data 
                                if list(i.items())[5][1] == status]

        return filtered_quiz_list



# Service for verification of quiz object about to be created
class QuizObjectVerification:
    # Denying object of its creating on specified condition
    def deny_quiz_object(self, error, object):
        object.objects.filter(id=self.id).delete()
        content = {'error': error}
        raise ValidationError(content, code=status.HTTP_400_BAD_REQUEST)