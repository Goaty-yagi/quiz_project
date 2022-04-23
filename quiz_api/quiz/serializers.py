from rest_framework import serializers
from django.db.models import F
from quiz.models import Quiz, Question, Answer, QuestionType, ParentField,QuizTaker,UserStatus

class AnswerListSerializer(serializers.ModelSerializer):
	# percantage = serializers.SerializerMethodField('get_percentage')
	class Meta:
		model = Answer
		fields = ["id", "question", "label", "is_correct",'answer_id','taken_num']

	# def get_percentage(self, obj):
	# 	answers = Answer.objects.filter(question_id=obj.question.id)
	# 	print("AOBJ",answers)
	# 	return 9090


class AnswerCountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = ["id", "question", "label", "is_correct",'answer_id','taken_num']		


class QuestionListSerializer(serializers.ModelSerializer):
	answer = AnswerListSerializer(many=True)
	# answers_count = serializers.SerializerMethodField()
	class Meta:
		model = Question
		fields = [
			"id",
			"quiz_level",
			"quiz", 
			"label", 
			"image", 
			"get_image", 
			'field', 
			'question_type',
			'status',
			'correct_answer', 
			'max_select',
			'taken_num',
			'answer']

	# def get_answers_count(self, obj):
	# 	return obj.answer_set.all().count()


class QuizListSerializer(serializers.ModelSerializer):
	# questions_count = serializers.SerializerMethodField()
	# question = QuestionListSerializer(many=True)
	class Meta:
		model = Quiz
		fields = ["id", "name", "description", "image", "slug","question" ]


class QuizNameIdListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Quiz
		fields = ["id", "name"]

	def to_representation(self, instance):
		rep = super(QuizNameIdListSerializer, self).to_representation(instance)
		rep['name'] = instance.name.name
		return rep


class FieldNameIdListSerializer(serializers.ModelSerializer):
	class Meta:
		model = ParentField
		fields = ["id", "name"]


class QuizFilterSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Quiz
		fields = ["id", "name", "description", "image", "slug" ]


class QuestionTypeSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = QuestionType
		fields = ["id", "name"]


class UserStatusSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = UserStatus
		fields = [
			"id",
			"status",
			"grade",
			"is_correct",
			"is_false",
			"percentage"]

	# def create(self, validated_data):
	# 		print('in__create')
	# 		liked_num_data = validated_data.pop('liked_num')
	# 		tag_data = validated_data.pop('tag')
	# 		liked_num_data = {}
	# 		question = BoardQuestion.objects.create(**validated_data)
	# 		user = validated_data.pop('user')
	# 		for tag in tag_data:
	# 			question.tag.add(tag)
	# 			if BoardUserTag.objects.filter(tag=tag, user=user).exists():
	# 				BoardUserTag.objects.update_or_create(
	# 					tag=tag,
	# 					user=user,
	# 					defaults={'used_num':F('used_num') + 1})
	# 				print("if done")
	# 			else:
	# 				BoardUserTag.objects.create(tag=tag, user=user, used_num=1)
	# 		BoardQuestionLiked.objects.create(question=question, **liked_num_data)
	# 		return question


class QuizTakerSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = QuizTaker
		fields = [
			"id", 
			"user", 
			"grade", 
			"level",
			"user_status",
			"test_take_num",
			"practice_take_num"]


	# def get_questions_count(self, obj):
	# 	return obj.question_set.all().count()

# class QuizFilteredSerializer(serializers.ModelSerializer):
# 	question = QuestionListSerializer(source='filtered_question',many=True, read_only=True)