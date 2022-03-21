from rest_framework import serializers
from user.models import User
from board.serializers import BoardAnswerReadSerializer, BoardQuestionListSerializer, BoardLikedReadSerializer, AnswerLikedCreateSerializer, UserTagSerializer, FavoriteQuestionSerializer

class UserSerializer(serializers.ModelSerializer):
    question = BoardQuestionListSerializer(many=True, required=False)
    answer = BoardAnswerReadSerializer(many=True, required=False)
    liked_num = BoardLikedReadSerializer(many=True, required=False)
    liked_answer = AnswerLikedCreateSerializer(many=True, required=False)
    user_tag = UserTagSerializer(many=True, required=False)
    favorite_question = FavoriteQuestionSerializer(many=True, required=False)
    
    class Meta:
        model = User
        fields = ["UID",
                  "name", 
                  "email", 
                  "grade", 
                  "thumbnail", 
                  "country",
                  "question", 
                  "answer",
                  "liked_num",
                  "liked_answer",
                  "user_tag",
                  "favorite_question"
                  ]
        # read_only_field = []