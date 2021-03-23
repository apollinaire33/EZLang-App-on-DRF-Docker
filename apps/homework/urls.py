from rest_framework import routers

from homework.views import (HomeworkAdministratingViewSet,
                            HomeworkViewSet, 
                            HomeworkTaskViewSet)


router = routers.DefaultRouter()

router.register(r'admin', HomeworkAdministratingViewSet)
router.register(r'', HomeworkViewSet)
router.register(r'task_load', HomeworkTaskViewSet)

urlpatterns = router.urls