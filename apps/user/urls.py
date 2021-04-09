from rest_framework import routers

from user.views import UserViewSet, SignupViewSet


router = routers.DefaultRouter()

router.register(r'user_list', UserViewSet, basename='user-list')
router.register(r'signup', SignupViewSet, basename='sign-up')

urlpatterns = router.urls