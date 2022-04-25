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
	user_status = UserStatusNameSerializer(many=True, read_only=True, required=False)
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