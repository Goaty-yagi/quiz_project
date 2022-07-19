from django.db import models

class Enquire(models.Model):
    user_name = models.CharField(max_length=20)
    email = models.EmailField(blank=False)
    enquire_type = models.CharField(max_length=100)
    enquire_content = models.CharField(max_length=1000)
    checked =models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ['-created_on',]

    def __str__(self):
        return self.user_name