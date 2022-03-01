from gettext import install
from pickletools import read_long1
from rest_framework import serializers
from board.models import BoardQuestion, BoardAnswer, BoardReply, BoardQuestionLiked

# from user.models import User
# from user.serializers import UserSerializer

class BoardLikedCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = BoardQuestionLiked
		fields = ["id",
				  "user", 
				  "question", 
				  "liked_num",
				  ]
		read_only_field = ['user',"question"]

		# def liked_count(self, instance):
		# 	return instance.liked_count()


class BoardLikedReadSerializer(serializers.ModelSerializer):
	class Meta:
		model = BoardQuestionLiked
		fields = ["id",
				  "user", 
				  "question", 
				  "liked_num",
				#   "liked_count"
				  ]
		read_only_field = ['user',"question"]
		depth=1


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
				  "reply",
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
	liked_num = BoardLikedReadSerializer(many=True, required=False)
	# viewed_count = serializers.SerializerMethodField()
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
				  "user",
				  "answer",
				  "img",
				  "viewed",
				  "liked_num",
				  "created_on", 
				#   "viewed_count",
				#   'replay_count'
				  ]
		depth=3
		

class BoardQuestionCreateSerializer(serializers.ModelSerializer):
	answer = BoardAnswerReadSerializer(many=True, required=False)
	liked_num = BoardLikedReadSerializer(required=False)
	# viewed_count = serializers.SerializerMethodField()
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
				  "user",
				  "answer",
				  "img",
				  "viewed",
				  "liked_num",
				  "created_on", 
				#   "viewed_count",
				#   'replay_count'
				  ]
	

	def create(self, validated_data):
			print('in__create')
			liked_num_data = validated_data.pop('liked_num')
			question = BoardQuestion.objects.create(**validated_data)
			BoardQuestionLiked.objects.create(question=question, **liked_num_data)
			return question