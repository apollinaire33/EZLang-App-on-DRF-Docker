from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserValidation:
    def email_exists( email):
        if User.objects.filter(email=email).exists():
            content = {'error': 'Email already exists'}
            raise ValidationError(content, code=status.HTTP_409_CONFLICT)

    def password_length(password):
        if len(password) < 6:
            content = {'error': 'Password must be at least 6 characters'}
            raise ValidationError(content, code=status.HTTP_409_CONFLICT)