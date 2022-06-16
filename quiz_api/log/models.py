from django.db import models


class Logger(models.Model):
    path = models.CharField(max_length=100, blank=True, null=True)
    message = models.CharField(max_length=200)
    actualErrorName = models.CharField(max_length=100, blank=True, null=True)
    actualErrorMessage  = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.message