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


class EnquireListApi(generics.ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = EnquireSerializer
    queryset = Enquire.objects.all()


# class EnquireDetailApi(generics.RetrieveUpdateDestroyAPIView):
#     pagination_class = PageNumberPagination
#     serializer_class = EnquireSerializer
#     queryset = Enquire.objects.all()


class EnquireDetailApi(APIView):
    def patch(self, request):
        print('patch',request)
        upd_loggers = []
        
        log_list = request.query_params['logList'].split()
        log_list = ''.join(log_list[0])
        log_list = log_list.split(',')
        logger_list = Enquire.objects.filter(id__in=log_list)
        for i in logger_list:
            i.checked = True
            upd_loggers.append(i)
        Enquire.objects.bulk_update(upd_loggers,fields=['checked'])
        print('return',upd_loggers)
        return Response("PATCH 200")