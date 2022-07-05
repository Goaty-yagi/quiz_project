from django.urls import path
from .apis import EnquireCreateApi, EnquireDetailApi


urlpatterns = [
  path('enquire/', EnquireCreateApi.as_view()),
  path('enquire-detail/', EnquireDetailApi.as_view()),
]