from email.policy import default
from user.models import User
from django.db import models
from django.db.models import Prefetch
from django.forms import BooleanField, DurationField
from django.utils.text import slugify
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

import uuid


class ParentQuiz(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_num_of_question(self):
        all_num_list = []
        quizzes = ParentQuiz.objects.values('id','name')
        fields = ParentField.objects.select_related('grade').all()
        questions = Question.objects.values('id','quiz','field')
        first_counter = 0
        for i in quizzes:
            counter = 0
            for k in [ field for field in fields if field.grade.name==i['name']]:
                if counter == 0: 
                    all_num_list.append({i['name']:{}})
                    all_num_list[first_counter][i['name']].update({k.name:len([ question for question in questions if question['field']==k.id])})
                    counter += 1
                else:
                    all_num_list[first_counter][i['name']].update({k.name:len([ question for question in questions if question['field']==k.id])})

            all_num_list[first_counter][i['name']].update({'sum':len([ question for question in questions if question['quiz']==i['id']])})
            first_counter += 1
        all_num_list.append({'all_questions_num':Question.objects.all().count()})
        return all_num_list


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

class ParentStatus(models.Model):
    name = models.CharField(max_length=100)
    grade = models.ForeignKey(ParentQuiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class ParentField(models.Model):
    name = models.CharField(max_length=100)
    grade = models.ForeignKey(ParentQuiz, on_delete=models.CASCADE)
    parent_status = models.ForeignKey(ParentStatus, default=1, blank=True, null=True, on_delete=models.CASCADE)

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
    field = models.ManyToManyField(ParentField, blank=True, null=True)
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
    question = models.ForeignKey(Question,related_name='answer', blank=True, null=True,  on_delete=models.CASCADE)
    label = models.CharField(max_length=100,blank=True, null=True)
    is_correct = models.BooleanField(default=False, blank=True, null=True)
    taken_num = models.IntegerField(default=0)
    answer_id = models.IntegerField(default=0, blank=True, null=True)
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
    max_grade = models.CharField(max_length=100, default=None, blank=True, null=True)
    max_level = models.IntegerField(default=0, null=True, blank=True)
    # user_status = models.ForeignKey(UserStatus, related_name='quiz_taker', default=None ,blank=True, on_delete=models.CASCADE)
    test_take_num = models.IntegerField(default=1)
    practice_take_num = models.IntegerField(default=0)
    

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        print('insave')
        if self.max_grade==None:
            self.max_grade = self.grade.name
            self.max_level = self.level
        else:
            if grade[self.grade.name] > grade[self.max_grade]:
                self.max_grade = self.grade.name
                self.max_level = self.level
            elif grade[self.grade.name] == grade[self.max_grade] and self.level > self.max_level:
                self.max_level = self.level
        super().save(*args, **kwargs)


class UserStatus(models.Model):
    quiz_taker = models.ForeignKey(QuizTaker,default=None, blank=True,null=True ,related_name='user_status', on_delete=models.CASCADE)
    status = models.ForeignKey(ParentStatus, blank=True,default=None ,on_delete=models.CASCADE)
    grade = models.ForeignKey(ParentQuiz,blank=True, on_delete=models.CASCADE)
    is_correct = models.IntegerField(default=0)
    is_false = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.is_correct == 0:
            self.percentage = 0
        elif(self.is_false == 0&self.is_correct > 0):
            self.percentage = 0
        else:
            self.percentage=(self.is_correct / (self.is_false + self.is_correct) * 100)
        super().save(*args, **kwargs)




class MyQuiz(models.Model):
    user = models.ForeignKey(User, related_name='my_quiz', on_delete=models.CASCADE)
    # question = models.ManyToManyField(Question, related_name='my_quiz')
    max_num = models.IntegerField(default=5)

    # timestamp = models.DateTimeField(auto_now_add=True, null=True)
        
    def __str__(self):
        return self.user.name


class MyQuestion(models.Model):
    my_quiz = models.ForeignKey(MyQuiz, null=True, related_name='my_question', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, blank=True, related_name='my_question',on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['timestamp',]

        
    # def __str__(self):
    #     return self.my_quiz
