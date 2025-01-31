from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import MockExam, MockExamQuestion, UserPerformance, User

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()  # For Google-authenticated users
        user.first_name = validated_data.get('first_name', '')
        user.last_name = validated_data.get('last_name', '')
        user.save()
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'photo']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        if 'photo' in validated_data:
            instance.photo = validated_data['photo']
        instance.save()
        return instance

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'photo', 'username']        

class MockExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockExam
        fields = ['id', 'user', 'subjects', 'start_time', 'duration', 'status']

class MockExamQuestionSerializer(serializers.ModelSerializer):
    # Add these nested fields to get the actual question data
    question = serializers.CharField(source='question.question')
    option_a = serializers.CharField(source='question.option_a')
    option_b = serializers.CharField(source='question.option_b')
    option_c = serializers.CharField(source='question.option_c')
    option_d = serializers.CharField(source='question.option_d')
    option_e = serializers.CharField(source='question.option_e', allow_null=True)
    correct_option = serializers.CharField(source='question.correct_option')
    explanation = serializers.CharField(source='question.explanation', allow_null=True)
    subject_id = serializers.IntegerField(source='question.subject_id')  # Add this line to include subject_id

    class Meta:
        model = MockExamQuestion
        fields = ['id', 'question', 'option_a', 'option_b', 'option_c', 
                  'option_d', 'option_e', 'correct_option', 'explanation', 
                  'user_answer', 'is_correct', 'subject_id']  # Add subject_id to the fields


        
class UserPerformanceSerializer(serializers.ModelSerializer):
    accuracy = serializers.ReadOnlyField()
    avg_time_per_question = serializers.ReadOnlyField()
    
    class Meta:
        model = UserPerformance
        fields = ['id', 'user', 'subject', 'topic', 'total_questions', 'correct_answers', 'time_spent', 'accuracy', 'avg_time_per_question']
