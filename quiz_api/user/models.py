from django.db import models


class User(models.Model):
    UID = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=20)
    email = models.EmailField(blank=False)
    grade = models.CharField(max_length=20)
    thumbnail = models.ImageField(blank=True, null=True, default='account/default.png')
    country = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name