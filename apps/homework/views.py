from django_filters import rest_framework as filters
from django.utils import timezone
from rest_framework import permissions
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from homework.serializers import (HomeworkSerializer, 
                                  HomeworkUpdateForUserSerializer)
from homework.models import Homework
from homework.services import UserMark, HomeworkObjectVerification


# Viewset for administrating all homeworks
class HomeworkAdministratingViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = (permissions.IsAdminUser, )
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_fields = ('status', )


# Viewset for listing homeworks by specific user
class HomeworkViewSet(viewsets.mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_fields = ('status', )

    def list(self, request, *args, **kwargs):
        HomeworkObjectVerification.catching_a_list_sneak(
            self, 
            request, 
            "Stop fooling around with other people's homework list! Shame on you!")
        homework_list = Homework.objects.filter(user=request.user.id)
        print(homework_list)
        for i in homework_list:
            if i.date_expiry < timezone.now():
                Homework.objects.filter(id=i.id).update(status='Failed',
                                                        mark=0)
                UserMark.common_hw_mark(request.user.id)
                print(i.date_expiry)

        serializer = self.get_serializer(homework_list, many=True)
        return Response(serializer.data)


# Viewset for loading task by user
class HomeworkTaskViewSet(viewsets.mixins.RetrieveModelMixin,
                          viewsets.mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkUpdateForUserSerializer
    permission_classes = (permissions.IsAuthenticated, )
    
    def retrieve(self, request, *args, **kwargs):
        HomeworkObjectVerification.catching_a_sneak(
            self, request, "Stop fooling around with other people's homework! Shame on you!")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        HomeworkObjectVerification.catching_a_sneak(
            self, request, "Stop fooling around with other people's homework! Shame on you!")
        return super().update(request, *args, **kwargs)
        