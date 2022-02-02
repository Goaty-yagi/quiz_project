from rest_framework import generics
from board.models import BoardQuestion, BoardAnswer
from board.serializers import BoardQuestionListSerializer, BoardAnswerListSerializer


class BoardQuestionList(generics.ListCreateAPIView):
    queryset = BoardQuestion.objects.all()
    serializer_class = BoardQuestionListSerializer


class BoardQuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoardQuestion.objects.all()
    serializer_class = BoardQuestionListSerializer
    lookup_field = 'slug'


class BoardAnswerList(generics.ListCreateAPIView):
    queryset = BoardAnswer.objects.all()
    serializer_class = BoardAnswerListSerializer