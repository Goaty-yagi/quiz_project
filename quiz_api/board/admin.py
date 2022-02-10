from django.contrib import admin
from .models import BoardQuestion, BoardAnswer, BoardReply


admin.site.register(BoardQuestion)
admin.site.register(BoardAnswer)
admin.site.register(BoardReply)
