from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(models.Model):
    UID = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=20)
    email = models.EmailField(blank=False)
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

