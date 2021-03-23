from django.db import models
from django.contrib.auth import get_user_model

from homework.enums import HomeworkStatus
from homework.services import UserMark

User = get_user_model()


class Homework(models.Model):
    task = models.TextField(default='')
    mark = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=HomeworkStatus.choices, 
                            default='Tasked')
    task_load = models.FileField(default='', upload_to='txts')
    desc_for_mark = models.TextField(default='')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, to_field='id', 
                            related_name='user_homework', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    date_expiry = models.DateTimeField(null=False, blank=False)

    # Checking the status of homework and update average homework mark if it is Finished
    def save(self, *args, **kwargs): 
        if self.status == 'Tasked':
            super().save(*args, **kwargs)
        elif self.status == 'Finished' or self.status == 'Failed':
            super().save(*args, **kwargs)
            UserMark.common_hw_mark(self.user.id)

    def __str__(self):
        return self.task
            

