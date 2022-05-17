from django.db.models import Prefetch
from django.db.models.query_utils import select_related_descend
from django.shortcuts import render
from django.db.models import Prefetch
from django.db.models import F
# import django_filters
from django.db.models import Max
from itertools import chain

import random
from django.http import Http404
from rest_framework.response import Response
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from quiz.models import Quiz, Question, Answer, QuestionType, ParentField, UserStatus, QuizTaker
from quiz.serializers import (
    QuizListSerializer, 
    QuestionListSerializer, 
    AnswerListSerializer, 
    QuizFilterSerializer, 
    QuestionTypeSerializer, 
    QuizNameIdListSerializer, 
    FieldNameIdListSerializer, 
    AnswerCountSerializer,
    UserStatusSerializer,
    QuizTakerSerializer,
    )


class QuestionListApi(APIView):
# this is for all indicate quiz, field and module
    def get(self, request, format=None):
        try:
            queryset = Question.objects.filter(quiz=request.query_params['quiz'],
            field=request.query_params['field'],
            module=request.query_params['module'])
            print('before quiznum')
            quiz_num = int(request.query_params['num'])
            print('After quiznum')
            question = queryset.filter(id__in=pick_random_object(queryset,quiz_num))
            print('random done')
            serializer = QuestionListSerializer(question, many=True)
            return Response(serializer.data)
        except Question.DoesNotExist:
            raise Http404

class QuizFilteredListApi(APIView):
# this is for only filtering specific quiz
    def get(self, request, format=None):
        try:
            queryset = Question.objects.filter(quiz=request.query_params['quiz'])
            quiz_num = int(request.query_params['num'])
            question = queryset.filter(id__in=pick_random_object(queryset,quiz_num))
            serializer = QuestionListSerializer(question, many=True)
            return Response(serializer.data)
        except Question.DoesNotExist:
            raise Http404

class FieldFilteredListApi(APIView):
# this is for only filtering specific field
    def get(self, request, format=None):
        queryset = Question.objects.filter(field=request.query_params['field'])
        quiz_num = int(request.query_params['num'])
        question = queryset.filter(id__in=pick_random_object(queryset,quiz_num))
        serializer = QuestionListSerializer(question, many=True)
        return Response(serializer.data)

class ModuleFilteredListApi(APIView):
# this is for only filtering specific module
    def get(self, request, format=None):
        queryset = Question.objects.filter(module=request.query_params['module'])
        quiz_num = int(request.query_params['num'])
        question = queryset.filter(id__in=pick_random_object(queryset,quiz_num))
        serializer = QuestionListSerializer(question, many=True)
        return Response(serializer.data)
    
def pick_random_object(queryset,quiz_num):
    """recive num and queryset which have specific range.
    get all ids in queryset then make new list which include 
    the num of ids to return.
    you can use this method for invocation like
    queryset.filter(id__in=pick_random_object(queryset,num)).order_by('?')"""

    print("in_random")
    num = quiz_num
    random_id_list = list()
    random_id = [i.id for i in queryset]
    # max_id = queryset.aggregate(max_id=Max("id"))['max_id']
    # while True:
        # pk = random.randint(0, max_id)
    random_id_list = random.sample(random_id,num)
    return random_id_list
        # if question:
        #     print(len(random_id_list))
        #     if len(random_id_list) == num:
        #         return random_id_list
        #     elif len(random_id_list) <= 1:
        #         random_id_list.append(question.id)
        #     elif len(random_id_list) >= 2:
        #         random_id_list.append(question.id)
        #         a = set(random_id_list)
        #         random_id_list = list(a)

class QuizListApi(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id',]
    pagination_class = None


class QuizNameIdListApi(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizNameIdListSerializer
    pagination_class = None


class FieldNameIdListApi(generics.ListAPIView):
    queryset = ParentField.objects.all()
    serializer_class = FieldNameIdListSerializer
    pagination_class = None


class OneQuestionApi(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['label',]
    pagination_class = None


class UserStatusCreateApi(generics.CreateAPIView):
    queryset = UserStatus.objects.select_related(
                'quiz_taker', 
                'status',
                'grade'
                )
    serializer_class = UserStatusSerializer
    pagination_class = None
# class AnswerCountApi(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Answer.objects.all()
#     serializer_class = AnswerCountSerializer
#     pagination_class = None


class AnswerCountApi(APIView):
    def patch(self, request):
        print("ACA",request)
        answer_id = request.query_params['answer']
        question_id = request.query_params['question']
        Question.objects.filter(id=question_id).update(taken_num=F('taken_num') + 1)
        answer_id_list = answer_id.split(',')
        Answer.objects.filter(id__in=answer_id_list).update(taken_num=F('taken_num') + 1)
        return Response("PATCH 200")


class QuizTakerTestPatchApi(APIView):
    def patch(self, request):
        quiz_taker_id = request.query_params['quiz_taker']
        grade = request.query_params['grade']
        level = request.query_params['level']
        QuizTaker.objects.filter(id=quiz_taker_id).update(
            test_take_num=F('test_take_num') + 1,
            grade=grade,
            level=level)
        return Response("PATCH 200")


class QuizTakerPracticePatchApi(APIView):
    def patch(self, request):
        quiz_taker_id = request.query_params['quiz_taker']
        QuizTaker.objects.filter(id=quiz_taker_id).update(
            practice_take_num=F('practice_take_num') + 1,
            )
        return Response("PATCH 200")

    

class QuizApi(APIView):
    def get(self, request):
        print("request",request)
        quiz_id = request.query_params['quiz']
        num = int(request.query_params['num'])
        # field_ids = request.query_params.getlist("field")
        if request.query_params.getlist("field"):
            f = [i.strip("[]") for i in request.query_params.getlist("field")if i is not ',']
            i = ''.join(f[0])
            field_list = i.split(',')
            # field_list = [int(i) for i in request.query_params.getlist("field")[0].strip("[]")if i is not ',']
            print(type(field_list),field_list)
            try:
                queryset = Question.objects.select_related(
                    'quiz', 
                    'question_type'
                    ).prefetch_related(
                        'field', 
                        'status', 
                        'answer', 
                        ).filter(field__in=field_list)
                question = queryset.filter(id__in=pick_random_object(queryset,num)).order_by('?')
                quiz_queryset  = Quiz.objects.filter(
                    id = quiz_id,
                    )
                print('got quiz_queryset')
                # quizn_queryset  = Quiz.objects.filter(
                #     answer__question__field__in = field_list
                # ).distinct()
                # union = list(chain(quiz_queryset, all_question))
                serializer = QuizFilterSerializer(quiz_queryset, many=True)
                serializer2 = QuestionListSerializer(question, many=True)
                union = list(chain(serializer.data, serializer2.data))
                return Response(union)
            except Quiz.DoesNotExist:
                raise Http404
        else:
            try:
                queryset = Question.objects.select_related(
                    'quiz', 
                    'question_type'
                    ).prefetch_related(
                        'field', 
                        'status', 
                        'answer', 
                        ).filter(quiz=quiz_id)
                question = queryset.filter(id__in=pick_random_object(queryset,num)).order_by('?')
                quiz_queryset  = Quiz.objects.filter(
                    id = quiz_id,
                    )
                print('got quiz_queryset')
                serializer = QuizFilterSerializer(quiz_queryset, many=True)
                serializer2 = QuestionListSerializer(question, many=True)
                union = list(chain(serializer.data, serializer2.data))
                return Response(union)
            except Quiz.DoesNotExist:
                raise Http404


class QuizTestApi(APIView):
    def get(self, request):
        print("request",request)
        quiz_id = request.query_params['quiz']
        num = 10
        level = request.query_params['level']
        print('quiz_id',quiz_id)
        try:
            queryset = Question.objects.select_related(
                'quiz', 
                'question_type'
                ).prefetch_related(
                    'field', 
                    'status', 
                    'answer', 
                    ).filter(quiz_level=level,quiz__name__id=quiz_id)
            question = queryset.filter(id__in=pick_random_object(queryset,num)).order_by('?')
            quiz_queryset  = Quiz.objects.filter(
                id = quiz_id,
                )
            print('got quiz_queryset')
            serializer = QuizFilterSerializer(quiz_queryset, many=True)
            serializer2 = QuestionListSerializer(question, many=True)
            union = list(chain(serializer.data, serializer2.data))
            return Response(union)
        except Quiz.DoesNotExist:
            raise Http404
        

    # def get(self, request, format=None):
    #     try:
    #         queryset = Quiz.objects.filter(quiz=request.query_params['quiz'],
    #         field=request.query_params['field'],
    #         module=request.query_params['module'])
    #         print('before quiznum')
    #         quiz_num = int(request.query_params['num'])
    #         print('After quiznum')
    #         question = queryset.filter(id__in=pick_random_object(queryset,quiz_num))
    #         print('random done')
    #         serializer = QuestionListSerializer(question, many=True)
    #         return Response(serializer.data)
    #     except Question.DoesNotExist:
    #         raise Http404


    # def pick_random_object(self):
    #     max_id = Quiz.objects.all().aggregate(max_id=Max("id"))['max_id']
    #     while True:
    #         pk = random.randint(1, max_id)
    #         quiz = Quiz.objects.filter(pk=pk).first()
    #         if quiz:
    #             return quiz.id

    # def get_queryset(self):
    #     quiz=self.queryset.filter(question__module__icontains='２課'
    #     ).distinct().prefetch_related(Prefetch('question', queryset=Question.objects.filter(module__icontains='２課')))
    #     return quiz


# class QuestionListApi(generics.ListAPIView):
#     queryset = Question.objects.filter(quiz='2')
#     serializer_class = QuestionListSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['quiz','field','module']

#     def pick_random_object(self):
#         random_id_list = list()
#         max_id = self.queryset.aggregate(max_id=Max("id"))['max_id']
#         while True:
#             pk = random.randint(0, max_id)
#             question = self.queryset.filter(pk=pk).first()
#             if question:
#                 if len(random_id_list) == 3:
#                     return random_id_list
#                 elif len(random_id_list) <= 1:
#                     random_id_list.append(question.id)
#                 elif len(random_id_list) >= 2:
#                     random_id_list.append(question.id)
#                     a = set(random_id_list)
#                     random_id_list = list(a)

#     def get_queryset(self):
#         return self.queryset.filter(id__in=self.pick_random_object())

class AnswerListApi(generics.ListAPIView):
    queryset = Answer.objects
    serializer_class = AnswerListSerializer
    pagination_class = None


class QuestionTypeApi(generics.ListAPIView):
    queryset = QuestionType.objects
    serializer_class = QuestionTypeSerializer
    pagination_class = None


class QuizTakerApi(generics.ListAPIView):
    queryset = QuizTaker.objects.all()
    serializer_class = QuizTakerSerializer
    pagination_class = None
    

class QuizTakerRetrieveApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuizTaker.objects.all()
    serializer_class = QuizTakerSerializer
    pagination_class = None
    lookup_field = 'id'

# #  test   
# class FieldModuleFiltersAPI(APIView):
#     def get(self, request, format=None):
#         num = int(request.query_params['num'])
#         queryset = Quiz.objects.filter(name=request.query_params['name'])
#         queryset = Quiz.objects.filter(question__id__in=self.pick_random_object(queryset,num),question__module__icontains=request.query_params['module'],question__field__icontains=request.query_params['field']
#         ).distinct().prefetch_related(Prefetch('question', queryset=Question.objects.filter(id__in=self.pick_random_object(queryset,num),module__icontains=request.query_params['module'],field__icontains=request.query_params['field'])))
#         print(dict(queryset))
#         # random_query = queryset.filter(question__id=12)
#         serializer = QuizListSerializer(queryset, many=True)
#         return Response(serializer.data)

    
    
#     def pick_random_object(self,queryset,quiz_num):
#         num = quiz_num
#         random_id_list = list()
#         max_id = Max(queryset[0].question__pk)
#         while True:
#             pk = random.randint(0, max_id)
#             question = queryset(pk=pk).first()
#             if question:
#                 if len(random_id_list) == num:
#                     return random_id_list
#                 elif len(random_id_list) <= 1:
#                     random_id_list.append(question.id)
#                 elif len(random_id_list) >= 2:
#                     random_id_list.append(question.id)
#                     a = set(random_id_list)
#                     random_id_list = list(a)

# class QuestionFiltersAPI(APIView):
#     def get(self, request, format=None):
#         queryset= Question.objects.distinct().all()
#         serializer = QuestionListWithQuizSerializer(queryset,many=True)
#         return Response(serializer.data)

    


    