from django.urls import path
from user.apis import UserList


urlpatterns = [
  path('user/', UserList.as_view()),
#   path('question/<slug>', ForumQuestionDetail.as_view())
]