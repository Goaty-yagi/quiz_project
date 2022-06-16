from django.urls import path
from log.apis import LoggerCreateApi, LoggerListApi, LoggerDetailApi

urlpatterns = [
  path('loggers-create', LoggerCreateApi.as_view()), 
  path('loggers-list', LoggerListApi.as_view()),
  path('loggers-detail/<id>', LoggerDetailApi.as_view()),  
]