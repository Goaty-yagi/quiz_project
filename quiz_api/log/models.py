from django.db import models
import datetime


class Logger(models.Model):
    path = models.CharField(max_length=100, blank=True, null=True)
    message = models.CharField(max_length=200)
    actualErrorName = models.CharField(max_length=100, blank=True, null=True)
    actualErrorMessage  = models.CharField(max_length=200, blank=True, null=True)
    checked = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.message