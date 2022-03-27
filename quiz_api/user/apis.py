from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import Http404

from user.models import User
from user.serializers import UserSerializer,UserStrageSerializer


class UserList(generics.ListCreateAPIView):
    # parser_classes = (MultiPartParser, FormParser)
    queryset = User.objects.select_related('favorite_question_set').all()
    serializer_class = UserSerializer
    lookup_field = 'UID'


class UserDetail(generics.RetrieveUpdateAPIView ):
    parser_classes = (MultiPartParser, FormParser)
    queryset = User.objects.all()
    serializer_class = UserStrageSerializer
    lookup_field = 'UID'


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





