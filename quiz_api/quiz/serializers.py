from rest_framework import serializers
from quiz.models import Quiz,Question,Answer

class AnswerListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = ["id", "question", "label", "is_correct",'answer_id']


class QuestionListSerializer(serializers.ModelSerializer):
	answer = AnswerListSerializer(many=True)
	# answers_count = serializers.SerializerMethodField()
	class Meta:
		model = Question
		fields = ["id", "quiz", "label", "image","get_image","order",'field','module','correct_answer','answer']

	# def get_answers_count(self, obj):
	# 	return obj.answer_set.all().count()


class QuizListSerializer(serializers.ModelSerializer):
	# questions_count = serializers.SerializerMethodField()
	# question = QuestionListSerializer(many=True)
	class Meta:
		model = Quiz
		fields = ["id", "name", "description", "image", "slug","question" ]

	# def get_questions_count(self, obj):
	# 	return obj.question_set.all().count()

# class QuizFilteredSerializer(serializers.ModelSerializer):
# 	question = QuestionListSerializer(source='filtered_question',many=True, read_only=True)