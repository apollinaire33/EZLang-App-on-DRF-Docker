from rest_framework import routers

from user.views import UserViewSet, SignupViewSet


router = routers.DefaultRouter()

router.register(r'user_list', UserViewSet)
router.register(r'signup', SignupViewSet)

urlpatterns = router.urls