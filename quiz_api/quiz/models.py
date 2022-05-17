from email.policy import default
from user.models import User
from django.db import models
from django.forms import BooleanField, DurationField
from django.utils.text import slugify
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

import uuid


class ParentQuiz(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    name = models.ForeignKey(ParentQuiz, on_delete=models.CASCADE)
    description = models.CharField(max_length=70)
    image = models.ImageField(blank=True)
    slug = models.SlugField(default=uuid.uuid4,)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    
    class Meta:
        ordering = ['timestamp',]
        verbose_name_plural = "Quizzes"

        
    def __str__(self):
        return self.description


class ParentField(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ParentStatus(models.Model):
    name = models.CharField(max_length=100)
    grade = models.ForeignKey(ParentQuiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class QuestionType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='question', on_delete=models.CASCADE)
    quiz_level = models.IntegerField(default=1)
    label = models.CharField(max_length=100)
    image = models.ImageField(upload_to='quizzes/', blank=True, null=True)
    field = models.ManyToManyField(ParentField)
    question_type = models.ForeignKey(QuestionType, max_length=50, null=True, blank=True, on_delete=models.CASCADE)
    status = models.ManyToManyField(ParentStatus, blank=True)
    correct_answer = models.JSONField(blank=True, null=True)
    max_select = models.IntegerField(default=0)
    taken_num = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    

    def __str__(self):
        return self.label

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''


class Answer(models.Model):
    question = models.ForeignKey(Question,related_name='answer', on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    taken_num = models.IntegerField(default=0)
    answer_id = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.label

# class CorrectAnswer(models.Model):
#     order = models.IntegerField(default=1)

grade = {
    "超初級": 0,
    "初級": 1,
    "中級": 2,
    "上級": 3,
}

class QuizTaker(models.Model):
    user = models.ForeignKey(User, null=True, related_name='quiz_taker', on_delete=models.CASCADE)
    grade = models.ForeignKey(ParentQuiz, null=True, on_delete=models.CASCADE)
    level = models.IntegerField(default=1, null=True, blank=True)
    max_grade = models.CharField(max_length=100, default=None, null=True)
    max_level = models.IntegerField(default=0, null=True, blank=True)
    # user_status = models.ForeignKey(UserStatus, related_name='quiz_taker', default=None ,blank=True, on_delete=models.CASCADE)
    test_take_num = models.IntegerField(default=1)
    practice_take_num = models.IntegerField(default=0)
    

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if self.max_grade==None:
            self.max_grade = self.grade.name
            self.max_level = self.level
        else:
            for i in grade:
                if i == self.max_grade:
                    if grade[i] < grade[self.grade.name]:
                        self.max_grade = self.grade.name
                        self.max_level = self.level
                    elif grade[i] == grade[self.grade.name]:
                        if self.max_level < self.level:
                            self.max_level = self.level
        super().save(*args, **kwargs)


class UserStatus(models.Model):
    quiz_taker = models.ForeignKey(QuizTaker,default=None, blank=True,null=True ,related_name='user_status', on_delete=models.CASCADE)
    status = models.ForeignKey(ParentStatus, blank=True,default=None ,on_delete=models.CASCADE)
    grade = models.ForeignKey(ParentQuiz,blank=True, on_delete=models.CASCADE)
    is_correct = models.IntegerField(default=0)
    is_false = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)
    

 
