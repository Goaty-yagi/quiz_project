from rest_framework import serializers
from quiz.models import Quiz, Question, Answer, QuestionType, ParentField

class AnswerListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = ["id", "question", "label", "is_correct",'answer_id']


class QuestionListSerializer(serializers.ModelSerializer):
	answer = AnswerListSerializer(many=True)
	# answers_count = serializers.SerializerMethodField()
	class Meta:
		model = Question
		fields = [
			"id", 
			"quiz", 
			"label", 
			"image", 
			"get_image", 
			'field', 
			'question_type',
			'status',
			'correct_answer', 
			'max_select',
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


	# def get_questions_count(self, obj):
	# 	return obj.question_set.all().count()

# class QuizFilteredSerializer(serializers.ModelSerializer):
# 	question = QuestionListSerializer(source='filtered_question',many=True, read_only=True)