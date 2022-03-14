from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime
import asyncio

import secrets
import dateutil.parser
from user.models import User


class BoardParentCenterTag(models.Model):
    parent_tag = models.CharField(max_length=200)
        

    def __str__(self):
        return self.parent_tag


class BoardCenterTag(models.Model):
    tag = models.CharField(max_length=200)
    # question = models.ManyToManyField(BoardQuestion, related_name="cnter_tag", default=None, blank=True)
    user = models.ManyToManyField(User, default=None, related_name="center_tag", blank=True)
    used_num = models.IntegerField(default=0)
    parent_tag = models.ForeignKey(BoardParentCenterTag, related_name="center_tag", on_delete=models.CASCADE)
        

    def __str__(self):
        return self.tag


# STATUS_CHOICES = (
#     ("used", "used"),
#     ("viewed", "viewed"),
# )


class BoardUserTag(models.Model):
    tag = models.ForeignKey(BoardCenterTag, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=None, related_name='user_tag', on_delete=models.CASCADE)
    used_num = models.IntegerField(default=0)
    viewed_num = models.IntegerField(default=0)
    # status_handle = models.CharField(max_length=100, choices=STATUS_CHOICES, default=None, null=True)


    # def save(self, *args, **kwargs):
    #     self.used_num +=1
    #     super().save(*args, **kwargs)
    #     print("insave",self.tag.id,self.user.UID)
    #     try:
    #         OBJ = BoardUserTag.objects.get(user=self.user.UID)
    #         print(OBJ)
    #         self.used_num +=1
    #         self.save()
    #         print("tryend")
    #     except:
    #         print("except")
    #         # super().save(*args, **kwargs)
        

    def __str__(self):
        return self.tag.tag

 
class BoardQuestion(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    slug = models.SlugField(null=False)
    user = models.ForeignKey(User, related_name='question', default=None, on_delete=models.CASCADE)
    solved = models.BooleanField(default=False)
    post_on_going = models.BooleanField(default=True)
    select_best_on_going = models.BooleanField(default=False)
    vote_on_going = models.BooleanField(default=False)
    vote = models.IntegerField(default=0)
    tag = models.ManyToManyField(BoardCenterTag, related_name='question')
    img = models.ImageField(blank=True, null=True)
    viewed = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)


    # def handle_post_on_going(self):
    #     self.post_on_going = False
	# 	# self.save()
    #     print('post_on_going')

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = secrets.token_urlsafe(64)
    #     super().save(*args, **kwargs)


    # def add_good(self):
    #     self.good += 1
    
    # def add_viewed(self):
    #     self.viewed += 1
    # @property
    # def answer(self):
    #     return self.answer_set.all()

    
    class Meta:
        ordering = ['-created_on',]

        
    def __str__(self):
        return self.title



class BoardAnswer(models.Model):
    question = models.ForeignKey(BoardQuestion, related_name='answer', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
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


class BoardQuestionLiked(models.Model):
    user = models.ManyToManyField(User, default=None, related_name='liked_num')
    question = models.ForeignKey(BoardQuestion, default=None, related_name='liked_num', on_delete=models.CASCADE)
    # answer = models.ForeignKey(BoardAnswer, default=None, related_name='liked', on_delete=models.CASCADE)
    liked_num = models.IntegerField(default=0)
        

    def __str__(self):
        return self.question.title


class BoardAnswerLiked(models.Model):
    user = models.ManyToManyField(User, default=None, related_name='liked_answer')
    answer = models.ForeignKey(BoardAnswer, related_name='liked_answer', on_delete=models.CASCADE)
    liked_num = models.IntegerField(default=0)
    

    # def __str__(self):
    #     return self.question.title




# @receiver(post_save, sender=BoardUserTag)
# def add_used_num(sender, instance, created, **kwargs):
#     print(kwargs["signal"].__dict__, 'instance',instance.tag.id, 'sender',sender)  
#     try:
#         center_tag_id = instance.tag.id
#         center_tag_object = BoardCenterTag.objects.get(id=center_tag_id)
#         center_tag_object.used_num +=1
#         instance.used_num +=1
#         center_tag_object.save()
#     except:
#         raise Exception("unko")


# @receiver(post_save, sender=BoardQuestion)
# async def start_post_on_going(sender, instance, created, **kwargs):
#     print("receiver_dayo",kwargs["signal"].__dict__, 'instance',instance, 'sender',sender)  
#     if created:
#         schedOBJ = sched.scheduler()
#         week = 604800
#         schedOBJ.enter(20,1, instance.handle_post_on_going)
#         schedOBJ.run()
    # try:
    #     center_tag_id = instance.tag.id
    #     center_tag_object = BoardCenterTag.objects.get(id=center_tag_id)
    #     center_tag_object.used_num +=1
    #     instance.used_num +=1
    #     center_tag_object.save()
    # except:
    #     raise Exception("unko")
