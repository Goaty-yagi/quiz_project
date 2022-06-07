from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import Http404



class User(models.Model):
    UID = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=20)
    email = models.EmailField(blank=False)
    country = models.CharField(max_length=100, blank=True, null=True)
    thumbnail = models.ImageField(blank=True, null=True, default='account/default.png')
    # IP = models.ForeignKey(IPData, related_name='user', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class IPData(models.Model):
    user = models.ForeignKey(User,null=True,related_name='ip_data', on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    loc = models.CharField(max_length=100)
    org = models.CharField(max_length=100)
    postal = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    timezone = models.CharField(max_length=100)

    # def save(self, *args, **kwargs):
    #     print('ip_save',self.user.id)
    #     if self.user.country == False:
    #         self.user.country = self.country
    #         super().save(*args, **kwargs)

@receiver(post_save, sender=IPData)
def handle_on_reply(sender, instance, created, **kwargs):
    print('IIIInstance',instance,'cCCCreated',created, 'SSSsender',sender)  
    if created == True:
        print("CREATED",instance.country)
        try:
            user = User.objects.get(UID=instance.user.UID)
            if user.country:
                None
            else:
                user.country = instance.country
                user.save()
        except:
            raise Http404