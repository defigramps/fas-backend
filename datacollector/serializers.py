from rest_framework import serializers
from .models import Curriculum, Subject, Topic, Subtopic, SubtopicContent, PracticeQuestion, PastQuestion

class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class SubtopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtopic
        fields = '__all__'


class SubtopicContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubtopicContent
        fields = '__all__'


class PracticeQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeQuestion
        fields = '__all__'


class PastQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastQuestion
        fields = '__all__'

    def validate(self, data):
        if data.get('is_theory'):
            if not data.get('question'):
                raise serializers.ValidationError({"question": "Theory questions require a question field."})
        else:
            required_fields = ['option_a', 'option_b', 'option_c', 'option_d', 'correct_option']
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                raise serializers.ValidationError({field: f"{field} is required for MCQs." for field in missing_fields})
        return data