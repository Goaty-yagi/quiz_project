from django.db import models
from datetime import datetime
import secrets
import dateutil.parser
from user.models import User

 
class BoardQuestion(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=70)
    slug = models.SlugField(default='')
    user = models.ForeignKey(User, related_name='question', default=None, on_delete=models.CASCADE)
    solved = models.BooleanField(default=False)
    good = models.IntegerField(default=0)
    tag = models.CharField(max_length=20, blank=True)
    vote = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = secrets.token_urlsafe(64)
        super().save(*args, **kwargs)


    def add_good(self):
        self.good += 1
    
    # @property
    # def answer(self):
    #     return self.answer_set.all()

    
    class Meta:
        ordering = ['created_on',]

        
    def __str__(self):
        return self.title



class BoardAnswer(models.Model):
    question = models.ForeignKey(BoardQuestion, related_name='answer', on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(User, default=None, related_name='answer', on_delete=models.CASCADE)
    best = models.BooleanField(null=True)
    good = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['created_on',]

        
    def __str__(self):
        return self.description


class BoardReply(models.Model):
    answer = models.ForeignKey(BoardAnswer, related_name='reply', on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(User, default=None, related_name='reply', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['created_on',]

        
    def __str__(self):
        return self.description