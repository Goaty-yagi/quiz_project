from django.urls import path
from .apis import EnquireCreateApi, EnquireDetailApi, EnquireListApi


urlpatterns = [
  path('enquire/', EnquireCreateApi.as_view()),
   path('enquire-list/', EnquireListApi.as_view()),
  path('enquire-detail/', EnquireDetailApi.as_view()),
]