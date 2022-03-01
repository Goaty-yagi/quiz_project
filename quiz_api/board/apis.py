from rest_framework import generics
from board.models import BoardQuestion, BoardAnswer, BoardReply, BoardQuestionLiked
from board.serializers import BoardQuestionListSerializer, BoardAnswerReadSerializer, BoardAnswerCreateSerializer, BoardReplyCreateSerializer, BoardReplyReadSerializer, BoardQuestionCreateSerializer, BoardLikedCreateSerializer, BoardLikedReadSerializer


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

# class QuestionLikedRead(generics.ListAPIView):
#     queryset = BoardQuestionLiked.objects.all()
#     serializer_class = BoardLikedReadSerializer


# class QuestionLikedCreate(generics.CreateAPIView):
#     queryset = BoardQuestionLiked.objects.all()
#     serializer_class = BoardLikedCreateSerializer