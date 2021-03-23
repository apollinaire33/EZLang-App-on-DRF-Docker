from django.db import models


class HomeworkStatus(models.TextChoices):
    TASKED = "Tasked"
    FINISHED = "Finished"
    FAILED = "Failed"
    