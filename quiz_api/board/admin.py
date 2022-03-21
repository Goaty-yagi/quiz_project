from django.contrib import admin
from .models import BoardQuestion, BoardAnswer, BoardReply, BoardQuestionLiked, BoardAnswerLiked, BoardParentCenterTag, BoardCenterTag, BoardUserTag, UserFavoriteQuestion


admin.site.register(BoardQuestion)
admin.site.register(BoardAnswer)
admin.site.register(BoardReply)
admin.site.register(BoardQuestionLiked)
admin.site.register(BoardAnswerLiked)
admin.site.register(BoardParentCenterTag)
admin.site.register(BoardCenterTag)
admin.site.register(BoardUserTag)
admin.site.register(UserFavoriteQuestion)
