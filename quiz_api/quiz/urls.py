from django.urls import path, include
# from rest_framework import routers
from rest_framework_nested import routers
from quiz.apis import (
  QuizListApi, 
  QuestionListApi, 
  AnswerListApi, 
  FieldFilteredListApi, 
  ModuleFilteredListApi, 
  QuizFilteredListApi, 
  OneQuestionApi, 
  QuizApi,
  QuestionTypeApi,
  QuizNameIdListApi,
  FieldNameIdListApi,
  QuizTestApi,
  AnswerCountApi,
  UserStatusCreateApi,
  QuizTakerApi,
  QuizTakerTestPatchApi
  )


# router = routers.SimpleRouter()
# router.register(r'quizzes', QuizListApi)

# question_router = routers.NestedSimpleRouter(
#     router,
#     r'quizzes',
#     lookup='quiz')

# question_router.register(
#     r'question',
#     QuestionListApiView,
#     basename='quiz-question'
# )


urlpatterns = [
  path('quizzes/', QuizListApi.as_view()),
  path('quizzes-questions/', QuizApi.as_view()),
  path('quizzes-tests/', QuizTestApi.as_view()),
  path('quizzes-name-id/', QuizNameIdListApi.as_view()),
  path('questions/', QuestionListApi.as_view()),
  path('question-types/', QuestionTypeApi.as_view()),
  path('questions/quizzes/', QuizFilteredListApi.as_view()),
  path('questions/fields/', FieldFilteredListApi.as_view()),
  path('questions/modules/', ModuleFilteredListApi.as_view()),
  path('answers/', AnswerListApi.as_view()),
  path('answers-count/', AnswerCountApi.as_view()),
  path('quiz-taker/', QuizTakerApi.as_view()),
  path('quiz-taker-test/', QuizTakerTestPatchApi.as_view()),
  path('user-status/', UserStatusCreateApi.as_view()),
  path('field-list/', FieldNameIdListApi.as_view()),
  path('onequestion/', OneQuestionApi.as_view()),
#   path(r'',include(router.urls)),
#   path(r'',include(question_router.urls))
]