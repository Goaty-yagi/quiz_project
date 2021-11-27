from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

class Quiz(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=70)
    image = models.ImageField(blank=True)
    slug = models.SlugField(blank=True)
    # roll_out = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = self.name
        super(Quiz, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['timestamp',]
        verbose_name_plural = "Quizzes"

        
    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='question', on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    image = models.ImageField(upload_to='quizzes/', blank=True, null=True)
    order = models.IntegerField(default=False)
    field = models.CharField(max_length= 50, blank=True)
    module = models.CharField(max_length=50, blank=True)
    correct_answer = models.JSONField()
    

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
    answer_id = models.IntegerField(default=1)

    def __str__(self):
        return self.label

# class CorrectAnswer(models.Model):
#     order = models.IntegerField(default=1)

 
class QuizTaker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    data_finished = models.DateTimeField
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

class UsersAnswer(models.Model):
    quiz_taker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.quiestion