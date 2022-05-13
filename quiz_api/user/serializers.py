from rest_framework import serializers
from user.models import User, IPData
from board.serializers import (
    BoardAnswerReadSerializer, 
    BoardAnswerStorageSerializer,
    BoardQuestionListSerializer, 
    BoardQuestionStorageSerializer,
    BoardLikedReadSerializer, 
    BoardLikedStorageSerializer,
    AnswerLikedCreateSerializer, 
    AnswerLikedStorageSerializer,
    UserTagReadSerializer, 
    UserTagStorageSerializer,
    FavoriteQuestionReadSerializer,
    FavoriteQuestionStorageSerializer
    )
from quiz.models import User, QuizTaker, UserStatus, ParentQuiz, ParentStatus
from quiz.serializers import QuizTakerSerializer,QuizTakerStorageSerializer


class IPDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPData
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    question = BoardQuestionListSerializer(many=True, required=False) #ForeignKey
    answer = BoardAnswerReadSerializer(many=True, required=False) #ForeignKey
    liked_num = BoardLikedReadSerializer(many=True, required=False) #ManyToManyField
    liked_answer = AnswerLikedCreateSerializer(many=True, required=False) #ManyToManyField
    user_tag = UserTagReadSerializer(many=True, required=False) #ForeignKey
    favorite_question = FavoriteQuestionReadSerializer(many=True, required=False) #ForeignKey
    quiz_taker = QuizTakerSerializer(many=True, required=False) #ForeignKey
    ip_data = IPDataSerializer(many=True,required=False) #ForeignKey
    
    
    class Meta:
        model = User
        fields = ["UID",
                  "name", 
                  "email", 
                  "thumbnail", 
                  "question", 
                  "answer",
                  "liked_num",
                  "liked_answer",
                  "user_tag",
                  "favorite_question",
                  "quiz_taker",
                  'ip_data'
                  ]
        # read_only_field = []

    def create(self, validated_data):
        try:
            print('create', validated_data)
            quiz_taker = validated_data.pop('quiz_taker')
            level = dict(quiz_taker[1])['level']
            user = User.objects.create(**validated_data)
            QuizTaker.objects.create(user=user, level=level, **quiz_taker[0])
            ip_data = validated_data.pop('ip_data')
            IPData.objects.create(user=user, **ip_data[0])
            return user
        except:
            # set 超初級 ids 変わる可能性あり
            # 7 = ボキャブラリー
            # 1 = ひらがな
            # 6 = カタカナ
            # 13 = 数字
            # grade 4 = 超初級
            print('create22', validated_data)
            ids = [7,1,6,13]
            ip_data = validated_data.pop('ip_data')
            user = User.objects.create(**validated_data)
            IPData.objects.create(user=user, **ip_data[0])
            print('before grade')
            grade = ParentQuiz.objects.get(id=4)
            quiz_taker = QuizTaker.objects.create(user=user, grade=grade)
            status = ParentStatus.objects.filter(id__in=ids)
            print('ready',status)
            for i in status:
                UserStatus.objects.create(quiz_taker=quiz_taker, status=i, grade=grade)
            return user


class UserStrageSerializer(serializers.ModelSerializer):
    question = BoardQuestionStorageSerializer(many=True, required=False) #ForeignKey
    answer = BoardAnswerStorageSerializer(many=True, required=False) #ForeignKey
    liked_num = BoardLikedStorageSerializer(many=True, required=False) #ManyToManyField
    liked_answer = AnswerLikedStorageSerializer(many=True, required=False) #ManyToManyField
    user_tag = UserTagStorageSerializer(many=True, required=False) #ForeignKey
    favorite_question = FavoriteQuestionStorageSerializer(many=True, required=False) #ForeignKey
    quiz_taker = QuizTakerStorageSerializer(many=True, required=False) #ForeignKey
    
    class Meta:
        model = User
        fields = ["UID",
                  "name", 
                  "thumbnail",
                  "question", 
                  "answer",
                  "liked_num",
                  "liked_answer",
                  "user_tag",
                  "favorite_question",
                  "quiz_taker"
                  ]



class SimpleUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["UID",
                  "name", 
                  
                  ]
# class UserStrageSerializer(serializers.ModelSerializer):
#     question = BoardQuestionListSerializer(many=True, required=False) #ForeignKey
#     answer = BoardAnswerReadSerializer(many=True, required=False) #ForeignKey
#     liked_num = BoardLikedReadSerializer(many=True, required=False) #ManyToManyField
#     liked_answer = AnswerLikedCreateSerializer(many=True, required=False) #ManyToManyField
#     user_tag = UserTagReadSerializer(many=True, required=False) #ForeignKey
#     favorite_question = FavoriteQuestionReadSerializer(many=True, required=False) #ForeignKey
#     quiz_taker = QuizTakerSerializer(many=True, required=False) #ForeignKey
    
#     class Meta:
#         model = User
#         fields = ["UID",
#                   "name", 
#                   "thumbnail",
#                   "country",
#                   "question", 
#                   "answer",
#                   "liked_num",
#                   "liked_answer",
#                   "user_tag",
#                   "favorite_question",
#                   "quiz_taker"
#                   ]