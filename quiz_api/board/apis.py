from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Max
import random
from django.http import Http404

from board.models import BoardQuestion, BoardAnswer, BoardReply, BoardQuestionLiked, BoardAnswerLiked, BoardParentCenterTag, BoardUserTag, BoardCenterTag
from board.serializers import BoardQuestionListSerializer, BoardAnswerReadSerializer, BoardAnswerCreateSerializer, BoardReplyCreateSerializer, BoardReplyReadSerializer, BoardQuestionCreateSerializer, BoardLikedCreateSerializer, BoardLikedReadSerializer, AnswerLikedReadSerializer, ParentTagSerializer, UserTagSerializer, CenterTagSerializer


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


class RelatedQuestionList(APIView):
# this is for all indicate quiz, field and module
    def get(self, request, format=None):
        request_tag_list = request.query_params.getlist("tag")
        try:
            solved_queryset = BoardQuestion.objects.filter(
                tag__in = request_tag_list,
                solved = True
            ).distinct()
            print("solved_queryset", solved_queryset)
            unsolved_queryset = BoardQuestion.objects.filter(
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


# set 3 unsolved questions and 12 solved questions
def set_random_object(solved_queryset, unsolved_queryset):
    print("in set_random")
    random_id_list = list()
    max_solved_queryset_id = solved_queryset.aggregate(max_id=Max("id"))['max_id']
    max_unsolved_queryset_id = unsolved_queryset.aggregate(max_id=Max("id"))['max_id']
    if len(solved_queryset) >= 12:
        solved_queryset_num = 12
    else:
        solved_queryset_num = len(solved_queryset)

    if len(unsolved_queryset) >= 3:
        unsolved_queryset_num = 3
    else:
        unsolved_queryset_num = len(unsolved_queryset)
    # set 3 unsolved questions
    while len(random_id_list) != unsolved_queryset_num:
        pk = random.randint(0, max_unsolved_queryset_id)
        unsolved_question = unsolved_queryset.filter(pk=pk)
        if unsolved_question:
            random_id_list.append(unsolved_question[0])
     # set 12 solved questions
    while len(random_id_list) != solved_queryset_num + unsolved_queryset_num:
        print("loop2 start", len(random_id_list), solved_queryset_num)
        pk = random.randint(0, max_solved_queryset_id)
        solved_question = solved_queryset.filter(pk=pk)
        if solved_question:
            random_id_list.append(solved_question[0])
            print("loop2 end")
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