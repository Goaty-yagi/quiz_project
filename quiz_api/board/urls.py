from django.urls import path, include
# from rest_framework import routers
from rest_framework_nested import routers
from board.apis import BoardQuestionList, BoardQuestionDetail, BoardAnswerRead, BoardAnswerCreate, BoardReplyCreate, BoardReplyRead, BoardQuestionCreate, QuestionLikedRead, AnswerLikedRead, ParetTagList, UsertagCreate, CenterTagList


urlpatterns = [
  path('question/list', BoardQuestionList.as_view()),
  path('question/create', BoardQuestionCreate.as_view()),
  path('question/<slug>', BoardQuestionDetail.as_view()),
  path('answer/read', BoardAnswerRead.as_view()),
  path('answer/create', BoardAnswerCreate.as_view()),
  path('reply/read/', BoardReplyRead.as_view()),
  path('reply/create/', BoardReplyCreate.as_view()),
  path('question-liked/<pk>/', QuestionLikedRead.as_view()),
  path('answer-liked/<pk>/', AnswerLikedRead.as_view()),
  path('parent-tag/', ParetTagList.as_view()),
  path('center-tag/', CenterTagList.as_view()),  
  path('user_tag/create/', UsertagCreate.as_view()),

]