from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.services import UserValidation

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        UserValidation.password_length(password)
        user_obj = User(**validated_data)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'mark_hw', 'mark_tests')



