from this import d
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Q
from rest_framework import status
from django.db.models import Max
import random
import operator
import copy
from django.http import Http404

from board.models import BoardQuestion, BoardAnswer, BoardReply, BoardQuestionLiked, BoardAnswerLiked, BoardParentCenterTag, BoardUserTag, BoardCenterTag, User ,UserFavoriteQuestion
from board.serializers import BoardQuestionListSerializer, BoardAnswerReadSerializer, BoardAnswerCreateSerializer, BoardReplyCreateSerializer, BoardReplyReadSerializer, BoardQuestionCreateSerializer, BoardLikedCreateSerializer, BoardLikedReadSerializer, AnswerLikedReadSerializer, ParentTagSerializer, UserTagSerializer, CenterTagSerializer, FavoriteQuestionSerializer


class BoardQuestionList(generics.ListAPIView):
    queryset = BoardQuestion.objects.all()
    serializer_class = BoardQuestionListSerializer


class BoardQuestionCreate(generics.CreateAPIView):
    queryset = BoardQuestion.objects.all()
    serializer_class = BoardQuestionCreateSerializer


class BoardQuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoardQuestion.objects.all()
    serializer_class = BoardQuestionListSerializer
    lookup_field = 'slug'


class BoardAnswerRead(generics.ListAPIView):
    queryset = BoardAnswer.objects.all()
    serializer_class = BoardAnswerReadSerializer


class BoardAnswerCreate(generics.CreateAPIView):
    queryset = BoardAnswer.objects.all()
    serializer_class = BoardAnswerCreateSerializer


class BoardAnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoardAnswer.objects.all()
    serializer_class = BoardAnswerCreateSerializer
    lookup_field = 'id'


class BoardReplyRead(generics.ListAPIView):
    queryset = BoardReply.objects.all()
    serializer_class = BoardReplyReadSerializer


class BoardReplyCreate(generics.CreateAPIView):
    queryset = BoardReply.objects.all()
    serializer_class = BoardReplyCreateSerializer


class QuestionLikedRead(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoardQuestionLiked.objects.all()
    serializer_class = BoardLikedCreateSerializer


class AnswerLikedRead(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoardAnswerLiked.objects.all()
    serializer_class = AnswerLikedReadSerializer
    

class ParetTagList(generics.ListAPIView):
    queryset = BoardParentCenterTag.objects.all()
    serializer_class = ParentTagSerializer


class CenterTagList(generics.ListAPIView):
    queryset = BoardCenterTag.objects.all()
    serializer_class = CenterTagSerializer


class UsertagCreate(generics.CreateAPIView):
    queryset = BoardUserTag.objects.all()
    serializer_class = UserTagSerializer


class UsertagRead(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoardUserTag.objects.all()
    serializer_class = UserTagSerializer


class FavoriteQuestionUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserFavoriteQuestion.objects.all()
    serializer_class = FavoriteQuestionSerializer


class FavoriteQuestionCreate(generics.CreateAPIView):
    queryset = UserFavoriteQuestion.objects.all()
    serializer_class = FavoriteQuestionSerializer
    

# class AnsweredQuestionList(generics.ListAPIView):
    # serializer_class = BoardQuestionListSerializer

    # def get_queryset(self):
    #     user = User.objects.filter(user=self.request.user)
    #     return BoardQuestion.objects.filter(UID=user)

class AnsweredQuestionList(APIView):
# get questions from user UID in answer
    def get(self, request, format=None):
        user = request.query_params.getlist("user")
        try:
            question  = BoardQuestion.objects.filter(
                answer__user = user[0],
            ).distinct()
            serializer = BoardQuestionListSerializer(question, many=True)
            return Response(serializer.data)
        except BoardQuestion.DoesNotExist:
            raise Http404


class favoriteQuestionList(APIView):
# get questions from user UID in answer
    def get(self, request, format=None):
        print("request",request)
        question_id = request.query_params.getlist("question_id")[0].split(",")
        print(type(question_id),question_id)
        try:
            question  = BoardQuestion.objects.filter(
                id__in = question_id
            ).distinct()
            serializer = BoardQuestionListSerializer(question, many=True)
            return Response(serializer.data)
        except BoardQuestion.DoesNotExist:
            raise Http404


class RelatedQuestionList(APIView):
    """recieve 1 ~ 3 tag_ids and UID. get queryset exclude UID question 
    and filtered tag_id and solved status. then go to set_random_question function"""
    def get(self, request, format=None):
        print("request",request)
        request_tag_list = request.query_params.getlist("tag")
        uid = request.query_params.getlist("uid")[0]
        print("uid",uid)
        try:
            solved_queryset = BoardQuestion.objects.exclude(user__UID=uid).filter(
                tag__in = request_tag_list,
                solved = True
            ).distinct()
            print("solved_queryset", solved_queryset)
            unsolved_queryset = BoardQuestion.objects.exclude(user__UID=uid).filter(
                tag__in = request_tag_list,
                solved = False
            ).distinct()
            question = set_random_object(solved_queryset, unsolved_queryset)
            # question = solved_queryset
            print(question)
            serializer = BoardQuestionListSerializer(question, many=True)
            return Response(serializer.data)
        except BoardQuestion.DoesNotExist:
            raise Http404


class SearchQuestionList(APIView):
    """ this is for search question.
    if len(request.data) == 1, search title, descroption, also 
    answer descrption and reply description 
    if len(request.data) > 1 search questions with first 2 keywords
    that have both on title or description, if no, search questions which
    has one of them.
    after that, search in the question searched above with third key
    if con't find any, forth key will be searched in the second round question list
    if fond forth one will be searched in the third list with."""
    def get(self, request, format=None):
        keywords = request.query_params.getlist("keyword")[0]
        keywords = keywords.split(',')
        all_question = BoardQuestion.objects.all()
        count = 0
        if len(keywords) < 2:
            question1 = all_question.filter(Q(title__icontains=keywords[0]) | Q(description__icontains=keywords[0])).distinct()
            question2 = all_question.filter(Q(answer__reply__description__icontains=keywords[0]) | Q(answer__description__icontains=keywords[0])).distinct()
            question = question1 | question2
            print(question1 , question2 , question)
            serializer = BoardQuestionListSerializer(question, many=True)
            return Response(serializer.data)
        for keynum in range(len(keywords)):
            print(keywords[keynum])
            if count == 0:
                # question1 = all_question.filter(Q(title__icontains=key1) & Q(description__icontains=key2))
                count += 1
            elif count == 1:
                question1 = all_question.filter(
                Q(title__icontains=keywords[0]) & Q(title__icontains=keywords[keynum]) 
                ).distinct()
                question2 = all_question.filter(
                Q(description__icontains=keywords[0]) & Q(description__icontains=keywords[keynum])
                ).distinct()
                question = question1 | question2
                print(question.exists())
                if question.exists() == False:
                    question1 = all_question.filter(
                    Q(title__icontains=keywords[0]) | Q(title__icontains=keywords[keynum]) 
                    ).distinct()
                    question2 = all_question.filter(
                    Q(description__icontains=keywords[0]) | Q(description__icontains=keywords[keynum])
                    ).distinct()
                    question = question1 | question2
                submit_question = copy.deepcopy(question)
                count += 1
            elif count >= 2:
                temporary_question = copy.deepcopy(submit_question)
                submit_question = submit_question.filter(Q(title__icontains=keynum) | Q(description__icontains=keywords[keynum])).distinct()
                if submit_question.exists == False:
                    submit_question = temporary_question
                if count == len(keywords)-1 and submit_question.exists()==False:
                    submit_question = temporary_question
                    if temporary_question.exists() == False:
                        submit_question = question
        serializer = BoardQuestionListSerializer(submit_question, many=True)
        return Response(serializer.data)

# class Conbine():
#     def __init__(self, keywords=''):
#         string = ''
#         keywords = keywords

#     def __add__(self, other):
#         return self.string + other.string

# def conbine_Q(keywords):
#     filter_operator = {
#         "&": operator.and_,
#         "|": operator.or_
#     }
#     Q_filter = Q(title__icontains="{}").format() 
#     Q_dict = dict()
#     # for k in range(len(keywords)):
#     for i in keywords:
#         Q_dict[i] = Q(title__icontains="{i}").format() + filter_operator["&"]()


        # request_tag_list = request.query_params.getlist("tag")
        # try:
        #     solved_queryset = BoardQuestion.objects.filter(
        #         tag__in = request_tag_list,
        #         solved = True
        #     ).distinct()
        #     print("solved_queryset", solved_queryset)
        #     unsolved_queryset = BoardQuestion.objects.filter(
        #         tag__in = request_tag_list,
        #         solved = False
        #     ).distinct()
        #     question = set_random_object(solved_queryset, unsolved_queryset)
        #     # question = solved_queryset
        #     print(question)
        #     serializer = BoardQuestionListSerializer(question, many=True)
        #     return Response(serializer.data)
        # except BoardQuestion.DoesNotExist:
        #     raise Http404

# @api_view(['GET'])
# def search(request):
#     query = request.data.get('query', '')

#     if query:
#         question = BoardQuestion.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
#         serializer = BoardQuestionListSerializer(question, many=True)
#         return Response(serializer.data)
#     else:
#         return Response({"products": []})


# set 3 unsolved questions and 12 solved questions
def set_random_object(solved_queryset, unsolved_queryset):
    print("in set_random")
    unsolevd_list = [i for i in unsolved_queryset]
    solved_list = [i for i in solved_queryset]
    
    if len(solved_queryset) >= 12:
        solved_queryset_num = 12
    else:
        solved_queryset_num = len(solved_queryset)

    if len(unsolved_queryset) >= 3:
        unsolved_queryset_num = 3
    else:
        unsolved_queryset_num = len(unsolved_queryset)
    # set 3 unsolved questions
    random_id_list = random.sample(unsolevd_list, unsolved_queryset_num)
    # set 12 solved questions
    random_solved_list = random.sample(solved_list, solved_queryset_num)
    for solved_question in random_solved_list:
        random_id_list.append(solved_question)
    return random_id_list


# class RelatedQuestion(generics.ListAPIView):
#     queryset = BoardQuestion.objects.fi()
#     serializer_class = BoardQuestionListSerializer
#     lookup_field = 'slug'


# class UserTagCreateApi(APIView):
#     def post(self, request, format=None):
#         print("self",self.__dict__)
#         print("requesti",request)
#         serializer = UserTagSerializer(data=request.data)
#         print(serializer)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # try:
        #     queryset = BoardUserTag.objects.create(request,
        #     field=request.query_params['field'],
        #     module=request.query_params['module'])
        #     quiz_num = int(request.query_params['num'])
        #     question = queryset.filter(id__in=pick_random_object(queryset,quiz_num))
        #     serializer = QuestionListSerializer(question, many=True)
        #     return Response(serializer.data)
        # except Question.DoesNotExist:
        #     raise Http404

# class QuestionLikedRead(generics.ListAPIView):
#     queryset = BoardQuestionLiked.objects.all()
#     serializer_class = BoardLikedReadSerializer


# class QuestionLikedCreate(generics.CreateAPIView):
#     queryset = BoardQuestionLiked.objects.all()
#     serializer_class = BoardLikedCreateSerializer