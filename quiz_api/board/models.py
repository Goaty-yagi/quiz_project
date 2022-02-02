from django.db import models
from datetime import datetime
import uuid
import dateutil.parser

class User(models.Model):
    UID = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=20)
    email = models.EmailField()
    grade = models.CharField(max_length=20)
    country = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['name',]

        
    def __str__(self):
        return self.name

 
class BoardQuestion(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=70)
    slug = models.SlugField(blank=True)
    
    solved = models.BooleanField(default=False)
    good = models.IntegerField(default=0)
    tag = models.CharField(max_length=20, blank=True)
    vote = models.IntegerField(default=0)
    created_by = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        self.slug = uuid.uuid4()
        super(BoardQuestion, self).save(*args, **kwargs)


    def add_good(self):
        self.good += 1
    
    # @property
    # def answer(self):
    #     return self.answer_set.all()

    
    class Meta:
        ordering = ['created_by',]

        
    def __str__(self):
        return self.title



class BoardAnswer(models.Model):
    question = models.ForeignKey(BoardQuestion, related_name='answer', on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    
    best = models.BooleanField(null=True)
    good = models.IntegerField(default=0)
    created_by = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['created_by',]

        
    def __str__(self):
        return self.description


class BoardReply(models.Model):
    answer = models.ForeignKey(BoardAnswer, related_name='answer', on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    created_by = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['created_by',]

        
    def __str__(self):
        return self.description


class BoardReply2(models.Model):
    answer = models.ForeignKey(BoardAnswer, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    reply = models.ForeignKey(BoardReply,  on_delete=models.CASCADE)
    created_by = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['created_by',]

        
    def __str__(self):
        return self.description


