from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

from django.http import Http404
from django.db.models import Prefetch

import copy
# from ipware import get_client_ip

from user.models import User
from board.models import BoardQuestion, BoardAnswer
from user.serializers import UserSerializer,UserStrageSerializer, SimpleUserSerializer
from quiz.models import UserStatus, QuizTaker, ParentStatus, ParentQuiz
from quiz.serializers import UserStatusSerializer,QuizTakerSerializer

# class UserList(generics.ListCreateAPIView):
#     # parser_classes = (MultiPartParser, FormParser)
#     queryset = User.objects.select_related('favorite_question_set').all()
#     serializer_class = UserSerializer
#     lookup_field = 'UID'

class UserList(APIView):

    def post(self, request, format=None):
            print('API',request,request.data)
            if User.objects.filter(UID=request.data['UID']).exists():
                print('exists',User.objects.filter(UID=request.data['UID']).exists())
                return HttpResponse(status=404,content='user-exists-django')
            else:
                try:
                    user_status = copy.deepcopy(request.data["quiz_taker"][2])
                    grade = copy.deepcopy(request.data["quiz_taker"][0])
                    serializer = UserSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        print('saveed')
                        quiz_taker = dict(serializer.data['quiz_taker'][0])
                        quiz_taker_object = QuizTaker.objects.get(id=quiz_taker['id'])
                        parent_quiz = ParentQuiz.objects.get(id=grade['grade'])
                        for i in user_status["user_status"]:
                            parent_status = ParentStatus.objects.get(id=i['status'])
                            UserStatus.objects.create(
                                quiz_taker=quiz_taker_object,
                                status=parent_status,
                                grade=parent_quiz,
                                is_correct=i['isCorrect'],
                                is_false=i['isFalse'])
                        return Response(serializer.data)
                    else:
                        raise Http404
                except Exception as e:
                    if e.args[0] == 'quiz_taker':
                        serializer = UserSerializer(data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data)
                        else:
                            raise Http404
                    else:
                        raise e
            

class UserAllList(generics.ListCreateAPIView):
    # parser_classes = (MultiPartParser, FormParser)
    queryset = User.objects.all()
    serializer_class = SimpleUserSerializer


class UserDetail(generics.RetrieveUpdateAPIView ):
    parser_classes = (MultiPartParser, FormParser)
    pagination_class = None
    queryset = User.objects.prefetch_related(
        # Prefetch('question', queryset=BoardQuestion.objects.select_related('user').prefetch_related('tag'), to_attr="user_question"),
        'question',
        'question__tag',
        'question__tag__parent_tag',
        'question__tag__user',
        'question__user',
        'question__answer',
        'question__answer__question',
        'question__answer__question__user',
        'question__answer__question__tag',
        'question__answer__user',
        'question__answer__reply',
        'question__answer__reply__answer',
        'question__answer__reply__answer__user',
        'question__answer__reply__user',
        'question__answer__liked_answer',
        'question__answer__liked_answer__user',
        'question__answer__liked_answer__answer',
        'question__liked_num',
        'question__liked_num__user',
        'question__liked_num__question',
        'question__liked_num__question__user',
        'question__liked_num__question__tag',
        'answer',
        'answer__question',
        'answer__question__user',
        'answer__question__tag',
        'answer__user',
        'answer__reply',
        'answer__reply__answer',
        'answer__reply__answer__user',
        'answer__reply__user',
        'answer__liked_answer',
        'answer__liked_answer__user',
        'answer__liked_answer__answer',
        'user_tag',
        'user_tag__tag',
        'user_tag__tag__parent_tag',
        'user_tag__tag__user',
        'user_tag__user',
        'favorite_question',
        'favorite_question__user',
        'favorite_question__question',
        'favorite_question__question__user',
        'favorite_question__question__tag',
        'liked_num',
        'liked_num__user',
        'liked_num__question',
        'liked_num__question__user',
        'liked_num__question__tag',
        'liked_answer',
        'liked_answer__answer',
        'liked_answer__user',
        'quiz_taker',
        'quiz_taker__user',
        'quiz_taker__grade',
        'quiz_taker__user_status',
        )
        # Prefetch('answer', queryset=BoardAnswer.objects.select_related('user', 'question'), to_attr="user_answer"),        
    serializer_class = UserStrageSerializer
    lookup_field = 'UID'

# queryset = User.objects.prefetch_related(
#         'question',
#         'question__tag',
#         'question__tag__parent_tag',
#         'question__tag__user',
#         'question__user',
#         'question__answer',
#         'question__liked_num',
#         'question__liked_num__user',
#         'question__liked_num__question',
#         'question__liked_num__question__user',
#         'question__liked_num__question__tag',
#         'answer',
#         'answer__question',
#         'answer__question__user',
#         'answer__question__tag',
#         'answer__user',
#         'answer__liked_answer',
#         'user_tag',
#         'favorite_question',
#         'favorite_question__user',
#         'favorite_question__question',
#         'favorite_question__question__user',
#         'favorite_question__question__tag',
#         'liked_num',
#         'liked_answer')
# class UserDetail(APIView):
# # get questions from user UID in answer
#     def get(self, request, format=None):
#         print("in_get")
#         UID = request.query_params.getlist("user")
#         try:
#             user = User.objects.filter(
#                 UID=UID[0]
#             ).prefetch_related('favorite_question__question')
#             serializer = UserSerializer(user, many=True)
#             return Response(serializer.data)
#         except User.DoesNotExist:
#             raise Http404





