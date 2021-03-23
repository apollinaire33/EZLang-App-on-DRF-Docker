from django.contrib import admin

from quiz.models import Quiz, Question, Answer, QuizTaker, UserAnswer


admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuizTaker)
admin.site.register(UserAnswer)