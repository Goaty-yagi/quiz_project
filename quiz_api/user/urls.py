from django.urls import path
from user.apis import UserList, UserDetail, UserAllList


urlpatterns = [
  path('user/', UserList.as_view()),
  path('user-list/', UserAllList.as_view()),
  path('user/<UID>', UserDetail.as_view()),

#   path('question/<slug>', ForumQuestionDetail.as_view())
]