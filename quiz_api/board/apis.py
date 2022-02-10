from rest_framework import generics
from board.models import BoardQuestion, BoardAnswer, BoardReply
from board.serializers import BoardQuestionListSerializer, BoardAnswerReadSerializer, BoardAnswerCreateSerializer, BoardReplyCreateSerializer, BoardReplyReadSerializer


class BoardQuestionList(generics.ListCreateAPIView):
    queryset = BoardQuestion.objects.all()
    serializer_class = BoardQuestionListSerializer


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
