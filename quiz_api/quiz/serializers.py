from pkg_resources import require
from rest_framework import serializers
from django.db.models import F
from django.db.models import Count
from django.http import Http404

from quiz.models import Quiz, Question, Answer, QuestionType, ParentQuiz, ParentStatus, ParentField,QuizTaker,UserStatus, MyQuiz, MyQuestion

class AnswerListSerializer(serializers.ModelSerializer):
	# percantage = serializers.SerializerMethodField('get_percentage')
	class Meta:
		model = Answer
		fields = ["id", "question", "label", "is_correct",'answer_id','taken_num']


class AnswerCreateSerializer(serializers.ModelSerializer):
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

		def create(self, validated_data):
			print('IN_Answer-Create_serializer',validated_data)


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
			'answer',
			]

	# def get_answers_count(self, obj):
	# 	return obj.answer_set.all().count()

class QuestionDashboardSerializer(serializers.ModelSerializer):
	# answers_count = serializers.SerializerMethodField()
	class Meta:
		model = ParentQuiz
		fields = [
			'get_num_of_question']


class QuestionImageCreateSerializer(serializers.ModelSerializer):
	answer = AnswerListSerializer(many=True,required=False)

	class Meta:
		model = Question
		fields = [
			"id",
			"quiz_level",
			"quiz", 
			"label",
			'question_type',
			"image",
			'answer'
			]


class QuestionCreateSerializer(serializers.ModelSerializer):
	answer = AnswerListSerializer(many=True,required=False)
	
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
	
	def create(self, validated_data):
		print('IN_Create_serializer',validated_data)
		answers = validated_data.pop('answer')
		field = validated_data.pop('field')
		print('A',answers)
		print('F',field[0].parent_status.id)
		question = Question.objects.create(**validated_data)
		question.field.add(field[0])
		question.status.add(field[0].parent_status.id)
		print('Q',question,'A',answers)
		for answer in answers:
			Answer.objects.create(question=question, **answer)	
		return question

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
		fields = ["id", "name", "grade", "parent_status"]


class ParentStatusIdSerializer(serializers.ModelSerializer):
	class Meta:
		model = ParentStatus
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
	# percentage = serializers.SerializerMethodField()
	class Meta:
		model = UserStatus
		fields = [
			"id",
			"status",
			"quiz_taker",
			"grade",
			"is_correct",
			"is_false",
			"percentage"
			]

	# def get_percentage(self, obj):
	# 	print("obj",obj[0].is_correct)
	# 	if obj[0].is_correct==0:
	# 		return 0
	# 	elif obj[0].is_false==0:
	# 		return 10
	# 	else:
	# 		return int(obj[0].is_correct / (obj[0].is_false + obj[0].is_correct) * 10)


	def create(self, validated_data):
		print('IN_US_serializer',validated_data)
		is_correct = validated_data.pop('is_correct')
		is_false = validated_data.pop('is_false')
		
		if UserStatus.objects.filter(**validated_data).exists():
			if is_correct:
				user_status = UserStatus.objects.filter(**validated_data).update(
					is_correct=F('is_correct') + 1,
					percentage=((F('is_correct')+ 1) * 100 / ((F('is_correct')+ 1) + F('is_false'))))
				
			elif is_false:
				user_status = UserStatus.objects.filter(**validated_data).update(
					is_false=F('is_false') + 1,
					percentage=((F('is_correct')) * 100 / ((F('is_false')+ 1)+F('is_correct'))))
		else:
			if is_correct:
				user_status = UserStatus.objects.create(
					**validated_data,
					is_correct=is_correct,
					percentage=100)
			elif is_false:
				user_status = UserStatus.objects.create(
					**validated_data,
					is_false=is_false)
		return user_status
		
		
class UserStatusNameSerializer(serializers.ModelSerializer):
	# percentage = serializers.SerializerMethodField()
	class Meta:
		model = UserStatus
		fields = [
			"id",
			"status",
			"quiz_taker",
			"grade",
			"is_correct",
			"is_false",
			"percentage"
			]
	
	def to_representation(self, instance):
		rep = super(UserStatusNameSerializer, self).to_representation(instance)
		rep['status'] = [instance.status.name,instance.status.id]
		return rep

class QuizTakerSerializer(serializers.ModelSerializer):
	# read_only on user_status deleted for user creation purpose
	user_status = UserStatusNameSerializer(many=True, required=False)
	class Meta:
		model = QuizTaker
		fields = [
			"id", 
			"user", 
			"grade",
			"max_grade",
			"level",
			"max_level",
			"user_status",
			"test_take_num",
			"practice_take_num"]


# here for user-storage purpose


class QuizTakerStorageSerializer(serializers.ModelSerializer):
	user_status = UserStatusNameSerializer(many=True, read_only=True, required=False)
	class Meta:
		model = QuizTaker
		fields = [
			"id", 
			"grade", 
			"max_grade",
			"level",
			"max_level",
			"user_status",
			"test_take_num",
			"practice_take_num"]


class MyQuestionReadSerializer(serializers.ModelSerializer):

	class Meta:
		model = MyQuestion
		fields = ["id",
				  "my_quiz",
				  "question",
				  "timestamp",
				  ]
		depth=1


class MyQuestionSerializer(serializers.ModelSerializer):

	class Meta:
		model = MyQuestion
		fields = ["id",
				  "my_quiz",
				  "question",
				  "timestamp",
				  ]
	
	def create(self, validated_data):
		print("create",validated_data)
		my_quiz = validated_data.pop('my_quiz')
		question = validated_data.pop('question')
		# my_question = MyQuestion.objects.filter(my_quiz=my_quiz,question__id=question.id).exists()
			
		# print(my_question)
		if MyQuestion.objects.filter(my_quiz=my_quiz,question__id=question.id).exists():
			my_question = MyQuestion.objects.get(my_quiz=my_quiz,question__id=question.id)
			my_question.delete()
			print('removed')
			return "deleted"
		else:
			num = MyQuiz.objects.annotate(Count('my_question'))
			print("num",int(num.values_list('my_question__count')[0][0]))
			# print("questionlen", my_quiz.objects.annotate(Count('my_question')))
			if int(num.values_list('my_question__count')[0][0]) >= my_quiz.max_num:
				print('max')
				return Http404
			else:
				print('created')
				return  MyQuestion.objects.create(my_quiz=my_quiz,question_id=question.id)



class MyQuizSerializer(serializers.ModelSerializer):
	my_question = MyQuestionReadSerializer(many=True, required=False)

	class Meta:
		model = MyQuiz
		fields = ["id",
				  "user",
				  "my_question",
				  "max_num",
				  ]
