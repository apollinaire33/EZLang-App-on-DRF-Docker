from rest_framework import routers

from homework.views import (HomeworkAdministratingViewSet,
                            HomeworkViewSet, 
                            HomeworkTaskViewSet)


router = routers.DefaultRouter()

router.register(r'admin', HomeworkAdministratingViewSet, basename='for-admin')
router.register(r'', HomeworkViewSet, basename='homework_list_for_user')
router.register(r'task_load', HomeworkTaskViewSet, basename='homework-task-loading')

urlpatterns = router.urls