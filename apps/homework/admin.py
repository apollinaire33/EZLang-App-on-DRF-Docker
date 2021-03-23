from django.contrib import admin

from homework.models import Homework


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'mark', 'status', 'task_load', 'desc_for_mark')


admin.site.register(Homework, HomeworkAdmin)