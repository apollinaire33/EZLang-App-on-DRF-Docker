from rest_framework import status
from rest_framework.exceptions import ValidationError


# Service class for filtering lists
class FilterList:
    # Service func for filtering list by requested user id
    def filtered_list(self, request, status):
        from quiz.models import Quiz, QuizTaker
        try:
            queryset = Quiz.objects.filter(quiztaker__user=request.user.id)
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            
            
            filtered_quiz_list = [i for i in serializer.data 
                                    if list(i.items())[5][1] == status]

            return filtered_quiz_list
        except QuizTaker.DoesNotExist:
            pass


# Service for verification of quiz object about to be created
class QuizObjectVerification:
    # Denying object of its creating on specified condition
    def deny_quiz_object(self, error, object):
        object.objects.filter(id=self.id).delete()
        content = {'error': error}
        raise ValidationError(content, code=status.HTTP_409_CONFLICT)