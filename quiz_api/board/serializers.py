from gettext import install
from pickletools import read_floatnl, read_long1
import secrets
from ssl import Purpose
from django.db.models import F
from rest_framework import serializers
from user.models import User
from board.models import BoardQuestion, BoardAnswer, BoardReply, BoardQuestionLiked, BoardAnswerLiked, BoardParentCenterTag, BoardCenterTag, BoardUserTag, UserFavoriteQuestion

# from user.models import User
# from user.serializers import UserSerializer



class AnswerLikedCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = BoardAnswerLiked
		fields = ["id",
				  "user", 
				  "answer", 
				  "liked_num",
				  ]
		read_only_field = ['user']


class AnswerLikedReadSerializer(serializers.ModelSerializer):
	class Meta:
		model = BoardAnswerLiked
		fields = ["id",
				  "user", 
				  "answer", 
				  "liked_num",
				  ]
		read_only_field = ['user']
		

		# def liked_count(self, instance):
		# 	return instance.liked_count()


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
	liked_answer = AnswerLikedCreateSerializer(required=False, many=True)
	class Meta:
		model = BoardAnswer
		fields = ["id",
				  "question", 
				  "description", 
				  "user",
				  "created_on",
				  "on_reply",
				  "best",
				  "reply",
				  "liked_answer"
				  ]
		read_only_field = ['questions', "liked_answer"]
		depth=1


class BoardAnswerCreateSerializer(serializers.ModelSerializer):
	# user = serializers.StringRelatedField(allow_null=False)
	liked_answer = AnswerLikedCreateSerializer(required=False,many=True)
	class Meta:
		model = BoardAnswer
		fields = ["id",
				  "question", 
				  "description", 
				  "user",
				  "created_on",
				  "on_reply",
				  "liked_answer",
				  "best",
				  ]
		read_only_field = ['questions',]


	def create(self, validated_data):
		print('in__create')
		print("valid",validated_data)
		liked_answer_data = validated_data.pop('liked_answer')
		print("liked_answer_data:",liked_answer_data)
		answer = BoardAnswer.objects.create(**validated_data)
		BoardAnswerLiked.objects.create(answer=answer)
		print('answer',type(answer))
		return answer

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
				  "select_best_on_going",
				  "post_on_going",
				  "vote_on_going",
				  "on_answer",
				  "on_reply",
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
				  "select_best_on_going",
				  "post_on_going",
				  "vote_on_going",
				  "on_answer",
				  "tag", 
				  "vote", 
				  "user",
				  "answer",
				  "img",
				  "viewed",
				  "liked_num",
				#   "viewed_count",
				#   'replay_count'
				  ]

	# BoardUserTag part is not relevent to BoardUserTag.create
	def create(self, validated_data):
			print('in__create')
			liked_num_data = validated_data.pop('liked_num')
			tag_data = validated_data.pop('tag')
			liked_num_data = {}
			question = BoardQuestion.objects.create(**validated_data)
			user = validated_data.pop('user')
			for tag in tag_data:
				question.tag.add(tag)
				if BoardUserTag.objects.filter(tag=tag, user=user).exists():
					BoardUserTag.objects.update_or_create(
						tag=tag,
						user=user,
						defaults={'used_num':F('used_num') + 1})
					print("if done")
				else:
					BoardUserTag.objects.create(tag=tag, user=user, used_num=1)
			BoardQuestionLiked.objects.create(question=question, **liked_num_data)
			return question


class UserTagReadSerializer(serializers.ModelSerializer):
	class Meta:
		model = BoardUserTag
		fields = ["id",
				  "tag",
				  "user",
				  "used_num",
				  "viewed_num",
				  "total_num"
				  ]
		read_only_field = ['tag','user']
		depth=1


class UserTagSerializer(serializers.ModelSerializer):
	class Meta:
		model = BoardUserTag
		fields = ["id",
				  "tag",
				  "user",
				  "used_num",
				  "viewed_num",
				  "total_num"
				  ]
		read_only_field = ['tag','user']
		
	# this create work only from 'user-tag/create/' 
	def create(self, validated_data):
		tag = validated_data.pop('tag')
		user = validated_data.pop('user')
		if BoardUserTag.objects.filter(tag=tag,user=user).exists():
				return BoardUserTag.objects.update_or_create(
					tag=tag,
					user=user,
					defaults={'viewed_num':F('viewed_num') + 1})
		else:
			return BoardUserTag.objects.create(tag=tag, user=user, viewed_num = 1)
			

class CenterTagSerializer(serializers.ModelSerializer):
	question = BoardQuestionCreateSerializer(many=True)
	class Meta:
		model = BoardCenterTag
		fields = ["id",
				  "tag",
				  "question",
				  "user",
				  "used_num",
				  "parent_tag" 
				  ]
		read_only_field = ['center_tag','user','question']


# class CenterOnlyTagSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = BoardCenterTag
# 		fields = ["id",
# 				  "tag",
# 				  ]


class ParentTagSerializer(serializers.ModelSerializer):
	center_tag = CenterTagSerializer(many=True)
	class Meta:
		model = BoardParentCenterTag
		fields = ["id",
				  "parent_tag",
				  "center_tag"
				  ]
		read_only_field = ['center_tag']


class FavoriteQuestionReadSerializer(serializers.ModelSerializer):
	# question = BoardQuestionListSerializer(many=True)
	class Meta:
		model = UserFavoriteQuestion
		fields = ["id",
				  "user",
				  "question",
				  ]
		# read_only_field = ['user','question']
		depth=1


	# def update(self, instance, validated_data):
	# 	print("updatedayo")
	# 	question_data = validated_data.pop("question")
	# 	question = instance.question



class FavoriteQuestionSerializer(serializers.ModelSerializer):
	# question = BoardQuestionListSerializer(many=True)
	class Meta:
		model = UserFavoriteQuestion
		fields = ["id",
				  "user",
				  "question",
				  ]
		# read_only_field = ['user','question']

	def create(self, validated_data):
		# this create is that recieve data of ManytoMany field and data of foregnkey field
		# update_or_create only with user(foregnkey) and add many data later
		# update_or_create returns tuple include object and boolean true(for create) or false(for update)
		print('in__create')
		print("valid",validated_data)
		user = validated_data.pop('user')
		question = validated_data.pop('question')
		favorite_question = UserFavoriteQuestion.objects.update_or_create(
			user=user
			)
		for Q in question:
			print("Q",Q.id)
			if UserFavoriteQuestion.objects.filter(user=user,question__id=Q.id).exists():
				favorite_question[0].question.remove(Q)
				print('removed')
				return favorite_question[0]
		favorite_question[0].question.add(Q)
		print('created')
		return favorite_question[0]
		


# fron here for user storage Purpose

class NonEmailUserSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = User
		fields = ["UID",
                  ]

class BoardQuestionStorageSerializer(serializers.ModelSerializer):
	user = NonEmailUserSerializer

	class Meta:
		model = BoardQuestion
		fields = ["id",
				  "title", 
				  "description", 
				  "slug", 
				  "solved",
				  "select_best_on_going",
				  "post_on_going",
				  "vote_on_going",
				  "on_answer",
				  "tag", 
				  "vote", 
				  "img",
				  "viewed",
				  "user",
				  "created_on", 
				  ]


class BoardAnswerStorageSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = BoardAnswer
		fields = ["id",
				  "question", 
				  "description", 
				  "created_on",
				  "on_reply",
				  "best",
				  ]
		read_only_field = ['questions']


class BoardLikedStorageSerializer(serializers.ModelSerializer):
	class Meta:
		model = BoardQuestionLiked
		fields = ["id",
				  "question", 
				  "liked_num",
				  ]
		read_only_field = ["question"]


class AnswerLikedStorageSerializer(serializers.ModelSerializer):
	class Meta:
		model = BoardAnswerLiked
		fields = ["id", 
				  "answer", 
				  "liked_num",
				  ]

class UserTagStorageSerializer(serializers.ModelSerializer):
	class Meta:
		model = BoardUserTag
		fields = ["id",
				  "tag",
				  "used_num",
				  "viewed_num",
				  "total_num"
				  ]
		read_only_field = ['tag']
		depth=1


class FavoriteQuestionStorageSerializer(serializers.ModelSerializer):
	# question = BoardQuestionListSerializer(many=True)
	class Meta:
		model = UserFavoriteQuestion
		fields = ["id",
				  "question",
				  ]


# user optimization end

# from here for board notifications

class AnswerAndReplyOnQuestionSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = BoardQuestion
		fields = ["id", 
				  "on_answer",
				  "on_reply",
				  ]


class ReplyOnAnswerSerializer(serializers.ModelSerializer):

	class Meta:
		model = BoardAnswer
		fields = ["id",
				  "on_reply",
				  ]