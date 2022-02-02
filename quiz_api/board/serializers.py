from pickletools import read_long1
from rest_framework import serializers
from board.models import User, BoardQuestion, BoardAnswer


class BoardUserListSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", 
				  "UID", 
				  "name", 
				  "email", 
				  "grade", 
				  "country"]


class BoardAnswerListSerializer(serializers.ModelSerializer):
	# id = serializers.IntegerField(required=False)
	class Meta:
		model = BoardAnswer
		fields = ["id",
				  "question", 
				  "description", 
				  "created_by",
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
	answer = BoardAnswerListSerializer(many=True, required=False)
	
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
				  "answer",
				  "created_by", 
				#   'replay_count'
				  ]
		depth=1
		
		# def get_replay_count(self, obj):
		# 	return obj.question_set.all().count()

		# def create(self, validated_data):
		# 	answer = validated_data.pop('answer')
		# 	question = BoardQuestion.objects.create(answer={}**validated_data)
		# 	# BoardAnswer.objects.create(question=question, **answer)
		# 	return question
