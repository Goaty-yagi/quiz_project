from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser

from user.models import User
from user.serializers import UserSerializer


class UserList(generics.ListCreateAPIView):
    # parser_classes = (MultiPartParser, FormParser)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'UID'


class UserDetail(generics.RetrieveUpdateAPIView ):
    parser_classes = (MultiPartParser, FormParser)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'UID'





