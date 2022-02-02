from django.urls import path, include
# from rest_framework import routers
from rest_framework_nested import routers
from board.apis import BoardQuestionList, BoardQuestionDetail, BoardAnswerList


urlpatterns = [
  path('question/', BoardQuestionList.as_view()),
  path('question/<slug>', BoardQuestionDetail.as_view()),
  path('answer/', BoardAnswerList.as_view()),
]