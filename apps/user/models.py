from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework import status
from rest_framework.response import Response


class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            content = {'error': 'Users must have an email address'}
            return Response(content, status=status.HTTP_409_CONFLICT)
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    mark_hw = models.FloatField(default=0)
    mark_tests = models.FloatField(default=0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email