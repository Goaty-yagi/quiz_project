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
from quiz.models import User, QuizTaker
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
            ip_data = validated_data.pop('ip_data')
            # print('create2', ip_data[0])
            quiz_taker = validated_data.pop('quiz_taker')
            level = dict(quiz_taker[1])['level']
            user = User.objects.create(**validated_data)
            QuizTaker.objects.create(user=user, level=level, **quiz_taker[0])
            IPData.objects.create(user=user, **ip_data[0])
            return user
        except:
            user = User.objects.create(**validated_data)
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