from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

from homework.models import UserMark 
from quiz.enums import QuizCategory, QuizStatus
from quiz.services import QuizObjectVerification

User = get_user_model()


class Quiz(models.Model):
    category = models.CharField(max_length=50, choices=QuizCategory.choices, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    date_expiry = models.DateTimeField()

    def __str__(self):
        return str(self.id)

    # Func for creating quiztakers for every user after every creating of Quiz model
    def save(self, *args, **kwargs): 
        super().save(*args, **kwargs)
        for i in User.objects.all():
            if not QuizTaker.objects.filter(user=i, quiz=self):
                QuizTaker.objects.create(user=i, quiz=self)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question = models.CharField(max_length=255, default='')
    value = models.IntegerField()

    def __str__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class QuizTaker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, to_field='id')
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=QuizStatus.choices, default='Tasked')
    date_finished = models.DateTimeField(null=True)
    date_started = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  f"{self.user.name} {self.quiz}"

    # Denying creating QuizTaker if specified user already comleted or failed this quiz
    def save(self, *args, **kwargs): 
        super().save(*args, **kwargs)
        current_quiz = QuizTaker.objects.filter(user=self.user, quiz=self.quiz)[0]
        if current_quiz and (current_quiz.status == 'Finished' or 
                            current_quiz.status == 'Failed'):
            QuizObjectVerification.deny_quiz_object(self, 
                                                    'You already completed this quiz!', 
                                                    QuizTaker)


class UserAnswer(models.Model):
    quiz_taker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.answer)

    def save(self, *args, **kwargs): 
        super().save(*args, **kwargs)
        quiz_questions = Question.objects.filter(quiz=self.question.quiz.id)
        current_quiz = self.quiz_taker.id
        quiz_answers_by_user = UserAnswer.objects.filter(quiz_taker=current_quiz)

        # Denying creating UserAnswer if specified quiz_taker's quiz do not match 
        # with specified question's quiz 
        if self.question.quiz.id != self.quiz_taker.quiz.id or self.answer.question.id != self.question.id:         
            QuizObjectVerification.deny_quiz_object(self, 'Wrong question or quiz!', 
                                                    UserAnswer)

        # Denying creating UserAnswer if specified quiz_taker is already Finished or Failed 
        elif self.quiz_taker.status == 'Finished' or self.quiz_taker.status == 'Failed':
            QuizObjectVerification.deny_quiz_object(self, 'You already completed this quiz!', 
                                                    UserAnswer)

        # Func for resulting and updating user's average mark,
        # when UserAnswer's amount equals amount of quiz questions
        elif len(quiz_questions) == len(quiz_answers_by_user):
            mark_list = [i.answer.question.value for i in quiz_answers_by_user 
                        if i.answer.is_correct is True]
            QuizTaker.objects.filter(quiz=self.question.quiz.id).update(status='Finished', 
                                                                        score=sum(mark_list), 
                                                                        date_finished=timezone.now())
            UserMark.common_quiz_mark(self.quiz_taker.user.id)       