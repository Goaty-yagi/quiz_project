from rest_framework import generics
from log.serializers import LoggerSerializer
from log.models import Logger


class LoggerCreateApi(generics.CreateAPIView):
    queryset = Logger.objects.all()
    serializer_class = LoggerSerializer


class LoggerListApi(generics.ListAPIView):
    queryset = Logger.objects.all()
    serializer_class = LoggerSerializer


class LoggerDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Logger.objects.all()
    serializer_class = LoggerSerializer
    lookup_field = 'id'