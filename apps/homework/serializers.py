from rest_framework import serializers

from homework.models import Homework


# Serializer for listing homeworks for certain user and updating for admin
class HomeworkSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'task', 'mark', 'status', 'task_load',
                 'desc_for_mark', 'user', 'created_at', 'date_expiry']
        model = Homework


# Serializer for updating for certain user
class HomeworkUpdateForUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Homework
        fields = ['id', 'task_load', 'user']
