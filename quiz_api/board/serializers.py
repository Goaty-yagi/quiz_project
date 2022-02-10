from pickletools import read_long1
from rest_framework import serializers
from board.models import BoardQuestion, BoardAnswer, BoardReply

# from user.models import User
# from user.serializers import UserSerializer


class BoardReplyReadSerializer(serializers.ModelSerializer):
	# user = serializers.StringRelatedField(allow_null=False)
	class Meta:
		model = BoardReply
		fields = ["id",
				  "answer", 
				  "description", 
				  "user",
				  "created_on",
				  ]
		read_only_field = ['answer',]
		depth=1


class BoardReplyCreateSerializer(serializers.ModelSerializer):
	# user = serializers.StringRelatedField(allow_null=False)
	class Meta:
		model = BoardReply
		fields = ["id",
				  "answer", 
				  "description", 
				  "user",
				  "created_on",
				  ]
		read_only_field = ['answer',]


class BoardAnswerReadSerializer(serializers.ModelSerializer):
	reply = BoardReplyReadSerializer(many=True)
	class Meta:
		model = BoardAnswer
		fields = ["id",
				  "question", 
				  "description", 
				  "user",
				  "created_on",
				  "best",
				  "reply"
				  ]
		read_only_field = ['questions',]
		depth=1

class BoardAnswerCreateSerializer(serializers.ModelSerializer):
	# user = serializers.StringRelatedField(allow_null=False)
	class Meta:
		model = BoardAnswer
		fields = ["id",
				  "question", 
				  "description", 
				  "user",
				  "created_on",
				  "best",
				  ]
		read_only_field = ['questions',]

	# def create(self, validated_data):
	# 		print('in__create')
	# 		question = validated_data.pop('question')
	# 		answer = BoardAnswer.objects.create(question=question,**validated_data)
	# 		# BoardAnswer.objects.create(question=question, **answer)
	# 		return answer
		


class BoardQuestionListSerializer(serializers.ModelSerializer):
	answer = BoardAnswerReadSerializer(many=True, required=False)
	# user = UserSerializer(required=True)
	
	class Meta:
		model = BoardQuestion
		fields = ["id", 
				  "title", 
				  "description", 
				  "slug", 
				  "solved", 
				  "good", 
				  "tag", 
				  "vote", 
				  "add_good",
				  "user",
				  "answer",
				  "created_on", 
				#   'replay_count'
				  ]
		# depth=1
		
		# def get_replay_count(self, obj):
		# 	return obj.question_set.all().count()

		# def create(self, validated_data):
		# 	answer = validated_data.pop('answer')
		# 	question = BoardQuestion.objects.create(answer={}**validated_data)
		# 	# BoardAnswer.objects.create(question=question, **answer)
		# 	return question

