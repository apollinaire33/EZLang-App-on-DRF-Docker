from django.db import models


class QuizCategory(models.TextChoices):
    IT = "IT"
    BUSINESS = "Business"
    TECH = "Tech"
    FOOD = "Food"
    PHILOSOPHY = "Philosophy"
    FASHION = "Fashion"


class QuizStatus(models.TextChoices):
    TASKED = "Tasked"
    FINISHED = "Finished"
    FAILED = "Failed"