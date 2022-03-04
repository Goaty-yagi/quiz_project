from django.contrib import admin
from .models import BoardQuestion, BoardAnswer, BoardReply, BoardQuestionLiked, BoardAnswerLiked


admin.site.register(BoardQuestion)
admin.site.register(BoardAnswer)
admin.site.register(BoardReply)
admin.site.register(BoardQuestionLiked)
admin.site.register(BoardAnswerLiked)
