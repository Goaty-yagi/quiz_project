from django.contrib import admin
from .models import BoardQuestion, BoardAnswer, BoardReply, BoardQuestionLiked


admin.site.register(BoardQuestion)
admin.site.register(BoardAnswer)
admin.site.register(BoardReply)
admin.site.register(BoardQuestionLiked)
