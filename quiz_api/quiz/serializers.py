from rest_framework import serializers
from django.db.models import F
from quiz.models import Quiz, Question, Answer, QuestionType, ParentField

class AnswerListSerializer(serializers.ModelSerializer):
	# percantage = serializers.SerializerMethodField('get_percentage')
	class Meta:
		model = Answer
		fields = ["id", "question", "label", "is_correct",'answer_id','taken_num','percantage']

	# def get_percentage(self, obj):
	# 	answers = Answer.objects.filter(question_id=obj.question.id)
	# 	print("AOBJ",answers)
	# 	return 9090


class AnswerCountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = ["id", "question", "label", "is_correct",'answer_id','taken_num']
		# lookup_field = 'id'


		# def update(self, instance, validated_data):
		# 	print("in_update",instance,validated_data)
		# 	question_id = validated_data.pop('question')
		# 	# instance.taken_num += 1
		# 	instance.update(taken_num=F('taken_num') + 1)
		# 	question = Question.objects.get(id=question_id).update(taken_num=F('taken_num') + 1)
		# 	instance.save()
		# 	question.save()
		


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


class QuizTakerSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = QuestionType
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