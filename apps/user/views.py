from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import viewsets, permissions

from homework.services import HomeworkObjectVerification
from user.serializers import UserCreateSerializer, UserSerializer 

User = get_user_model()


class SignupViewSet(viewsets.mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserViewSet(viewsets.mixins.RetrieveModelMixin,
                    viewsets.mixins.ListModelMixin,
                    viewsets.mixins.UpdateModelMixin,
                    viewsets.mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        HomeworkObjectVerification.catching_a_sneak(
            self, request, "Stop fooling around with other people's accounts! Shame on you!")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        HomeworkObjectVerification.catching_a_sneak(
            self, request, "Stop fooling around with other people's accounts! Shame on you!")
        return super().destroy(request, *args, **kwargs)



