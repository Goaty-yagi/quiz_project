from rest_framework import generics
from rest_framework.views import APIView
from log.serializers import LoggerSerializer
from log.models import Logger
from rest_framework.response import Response



class LoggerCreateApi(generics.CreateAPIView):
    queryset = Logger.objects.all()
    serializer_class = LoggerSerializer


class LoggerListApi(generics.ListAPIView):
    queryset = Logger.objects.all()
    serializer_class = LoggerSerializer


# class LoggerDetailApi(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Logger.objects.all()
#     serializer_class = LoggerSerializer
#     lookup_field = 'id'


class LoggerPatchApi(APIView):
    def patch(self, request):
        print('patch',request)
        upd_loggers = []
        # f = [i.strip("[]") for i in request.query_params.getlist("field")if i is not ',']
        #     i = ''.join(f[0])
            # field_list = i.split(',')
        log_list = request.query_params['logList'].split()
        log_list = ''.join(log_list[0])
        log_list = log_list.split(',')
        logger_list = Logger.objects.filter(id__in=log_list)
        for i in logger_list:
            i.checked = True
            upd_loggers.append(i)
        Logger.objects.bulk_update(upd_loggers,fields=['checked'])
        print('return',upd_loggers)
        return Response("PATCH 200")
    