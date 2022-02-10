from rest_framework import serializers
from user.models import User
from board.serializers import BoardAnswerReadSerializer, BoardQuestionListSerializer

class UserSerializer(serializers.ModelSerializer):
    question = BoardQuestionListSerializer(many=True, required=False)
    answer = BoardAnswerReadSerializer(many=True, required=False)
    
    class Meta:
        model = User
        fields = ["UID",
                  "name", 
                  "email", 
                  "grade", 
                  "thumbnail", 
                  "country",
                  "question", 
                  "answer"]
        # read_only_field = []