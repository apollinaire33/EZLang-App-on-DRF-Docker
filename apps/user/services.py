from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError


User = get_user_model()

# Service class for validation user parameters when registrating
class UserValidation:
    def password_length(password):
        if len(password) < 6:
            content = {'error': 'Password must be at least 6 characters'}
            raise ValidationError(content, code=status.HTTP_400_BAD_REQUEST)


# Service class for verification of User objects about to process
class UserObjectVerification:
    # Func for verification if current user is the owner of requested user detail
    def catching_a_sneak(self, request, error):
        instance = self.get_object()
        if instance.id != request.user.id and request.user.is_superuser is False:
            content = {
                "error": error
                }
            raise ValidationError(content, code=status.HTTP_400_BAD_REQUEST)