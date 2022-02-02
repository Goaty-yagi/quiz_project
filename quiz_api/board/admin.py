from django.contrib import admin
from .models import BoardQuestion, BoardAnswer ,User


admin.site.register(BoardQuestion)
admin.site.register(BoardAnswer)
admin.site.register(User)