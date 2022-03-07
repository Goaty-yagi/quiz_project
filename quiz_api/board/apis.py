from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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