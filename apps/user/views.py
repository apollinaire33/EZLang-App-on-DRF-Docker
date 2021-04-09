from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import viewsets, permissions

from user.services import UserObjectVerification
from user.serializers import UserCreateSerializer, UserSerializer 


User = get_user_model()

# Viewset for signing up a new user
class SignupViewSet(viewsets.mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


# Viewset for User model
class UserViewSet(viewsets.mixins.RetrieveModelMixin,
                  viewsets.mixins.ListModelMixin,
                  viewsets.mixins.UpdateModelMixin,
                  viewsets.mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # Prevent method if user updates another's account 
    def update(self, request, *args, **kwargs):
        UserObjectVerification.catching_a_sneak(
            self, request, "Stop fooling around with other people's accounts! Shame on you!")
        return super().update(request, *args, **kwargs)

    # Prevent method if user deletes another's account 
    def destroy(self, request, *args, **kwargs):
        UserObjectVerification.catching_a_sneak(
            self, request, "Stop fooling around with other people's accounts! Shame on you!")
        return super().destroy(request, *args, **kwargs)



