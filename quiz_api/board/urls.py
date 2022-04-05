from django.urls import path, include
# from rest_framework import routers
from rest_framework_nested import routers

from board.apis import (
    BoardQuestionList, 
    BoardQuestionDetail, 
    BoardAnswerRead, 
    BoardAnswerCreate, 
    BoardReplyCreate, 
    BoardReplyRead, 
    BoardQuestionCreate, 
    QuestionLikedRead, 
    AnswerLikedRead, 
    ParentTagList, 
    UsertagCreate, 
    CenterTagList, 
    UsertagRead, 
    RelatedQuestionList, 
    SearchQuestionList, 
    AnsweredQuestionList, 
    FavoriteQuestionUpdate, 
    FavoriteQuestionCreate, 
    favoriteQuestionList, 
    BoardAnswerDetail, 
    UserQuestionList, 
    TagQuestionList,
    # CenterOnlyTagList
    )


urlpatterns = [
  path('question/list', BoardQuestionList.as_view()),
  path('question/filter-list', RelatedQuestionList.as_view()),
  path('question/create', BoardQuestionCreate.as_view()),
  path('question/<slug>', BoardQuestionDetail.as_view()),
  path('question/search/',SearchQuestionList.as_view()),
  path('question-answered', AnsweredQuestionList.as_view()),
  path('question-favorite', favoriteQuestionList.as_view()),
  path('question-user-question', UserQuestionList.as_view()),
  path('tag-question', TagQuestionList.as_view()),
  path('answer/read', BoardAnswerRead.as_view()),
  path('answer/create', BoardAnswerCreate.as_view()),
  path('answer-detail/<id>', BoardAnswerDetail.as_view()),
  path('reply/read/', BoardReplyRead.as_view()),
  path('reply/create/', BoardReplyCreate.as_view()),
  path('question-liked/<pk>/', QuestionLikedRead.as_view()),
  path('answer-liked/<pk>/', AnswerLikedRead.as_view()),
  path('favorite-question/<pk>', FavoriteQuestionUpdate.as_view()),
  path('favorite-question-create/', FavoriteQuestionCreate.as_view()),
  path('parent-tag/', ParentTagList.as_view()),
  path('center-tag/', CenterTagList.as_view()),
#   path('center-only-tag/', CenterOnlyTagList.as_view()),  
  path('user-tag/create/', UsertagCreate.as_view()),
  path('user-tag/<pk>/', UsertagRead.as_view()),
]