from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .serializers import EnquireSerializer
from .models import Enquire



class EnquireCreateApi(generics.CreateAPIView):
    pagination_class = PageNumberPagination
    serializer_class = EnquireSerializer
    queryset = Enquire.objects.all()


class EnquireDetailApi(generics.RetrieveUpdateDestroyAPIView):
    pagination_class = PageNumberPagination
    serializer_class = EnquireSerializer
    queryset = Enquire.objects.all()