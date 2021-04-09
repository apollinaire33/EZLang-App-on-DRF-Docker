from rest_framework import serializers

from quiz.models import Quiz, Answer, Question, QuizTaker, UserAnswer


# Serizalizer for answers
class AnswerSerializer(serializers.ModelSerializer):

	class Meta:
		model = Answer
		fields = ['id', 'question', 'text', 'is_correct']


# Serizalizer for questions
class QuestionSerializer(serializers.ModelSerializer):
	answers = AnswerSerializer(read_only=True, many=True)

	class Meta:
		model = Question
		fields = ['id', 'quiz', 'question', 'value', 'answers']


# Serializers for answers of certain user and accuracy of this answer
class UserAnswerSerializer(serializers.ModelSerializer):

	class Meta:
		model = UserAnswer
		fields = ['id', 'quiz_taker', 'question', 'answer']


class UserAnswerIsCorrectSerializer(serializers.ModelSerializer):
	answer = AnswerSerializer(read_only=True)

	class Meta:
		model = UserAnswer
		fields = ['id', 'quiz_taker', 'question', 'answer']


# Seriazlizer for holder of quiz and its result for certain user
class QuizTakerSerializer(serializers.ModelSerializer):
	usersanswer_set = UserAnswerIsCorrectSerializer(read_only=True, many=True)

	class Meta:
		model = QuizTaker
		fields = '__all__'
	

# Serializer for quizes of requested user
class QuizUserSerializer(serializers.ModelSerializer):
	questions_count = serializers.SerializerMethodField()
	quiztaker_set = serializers.SerializerMethodField()
	status = serializers.SerializerMethodField()

	class Meta:
		model = Quiz
		fields = ['id', 'category', 'created_at', 'date_expiry', 
				  'questions_count', 'status', 'quiztaker_set']
		read_only_fields = ['questions_count']

	# Counting the number of questions in quiz
	def get_questions_count(self, obj):
		return obj.questions.all().count()

	# Non-model fields for quiztaker of quiz and its status for sertain user
	def get_quiztaker_set(self, obj):		
		quiztaker = QuizTaker.objects.get(user=self.context['request'].user.id, 
										  quiz=obj)
		serializer = QuizTakerSerializer(quiztaker)
		return serializer.data

	def get_status(self, obj):
		quiztaker = QuizTaker.objects.get(user=self.context['request'].user.id, 
										  quiz=obj)
		return quiztaker.status


# Serializer for administrating quizes by admin only
class QuizAdminSerializer(serializers.ModelSerializer):

	class Meta:
		model = Quiz
		fields = ['id', 'category', 'created_at', 'date_expiry']