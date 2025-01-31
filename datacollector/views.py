from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Curriculum, Subject, Topic, Subtopic, SubtopicContent, PracticeQuestion, PastQuestion
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import (
    CurriculumSerializer,
    SubjectSerializer,
    TopicSerializer,
    SubtopicSerializer,
    SubtopicContentSerializer,
    PracticeQuestionSerializer,
    PastQuestionSerializer,
)

class CurriculumListCreateView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        curricula = Curriculum.objects.all()
        serializer = CurriculumSerializer(curricula, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CurriculumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubjectListCreateView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, curriculum_id):
        subjects = Subject.objects.filter(curriculum_id=curriculum_id)
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

    def post(self, request, curriculum_id):
        data = request.data
        data['curriculum'] = curriculum_id
        serializer = SubjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TopicListCreateView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, subject_id):
        topics = Topic.objects.filter(subject_id=subject_id)
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

    def post(self, request, subject_id):
        data = request.data
        data['subject'] = subject_id
        serializer = TopicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SubtopicListCreateView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, topic_id):
        subtopics = Subtopic.objects.filter(topic_id=topic_id)
        serializer = SubtopicSerializer(subtopics, many=True)
        return Response(serializer.data)

    def post(self, request, topic_id):
        data = request.data
        data['topic'] = topic_id
        serializer = SubtopicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubtopicContentView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, subtopic_id):
        content = SubtopicContent.objects.filter(subtopic_id=subtopic_id)
        serializer = SubtopicContentSerializer(content, many=True)
        return Response(serializer.data)

    def post(self, request, subtopic_id):
        data = request.data.copy()
        data['subtopic'] = subtopic_id
        serializer = SubtopicContentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  


# class TopicContentView(APIView):
#     authentication_classes = []
#     permission_classes = []
#     parser_classes = [MultiPartParser, FormParser]  # Ensure handling of form data with files

#     def get(self, request, topic_id):
#         # Fetch content related to the topic
#         content = Topic.objects.filter(topic_id=topic_id)
#         serializer = TopicContentSerializer(content, many=True)
#         return Response(serializer.data)

#     def post(self, request, topic_id):
#         # Create a mutable copy of the data
#         data = request.data.copy()
#         data['topic'] = topic_id  # Add the topic ID to the data

#         serializer = TopicContentSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PracticeQuestionView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, topic_id):
        questions = PracticeQuestion.objects.filter(topic_id=topic_id)
        serializer = PracticeQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, topic_id):
        data = request.data
        data['topic'] = topic_id
        serializer = PracticeQuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PastQuestionView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        # Check for URL kwargs first
        subject_id = kwargs.get('subject_id')
        curriculum_id = kwargs.get('curriculum_id')
        year = kwargs.get('year')

        # If not in kwargs, check query parameters
        if not subject_id:
            subject_id = request.query_params.get('subject')
        if not curriculum_id:
            curriculum_id = request.query_params.get('curriculum')
        if not year:
            year = request.query_params.get('year')

        # Filter questions based on the provided parameters
        queryset = PastQuestion.objects.all()

        # Apply filters if provided
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        
        if curriculum_id:
            # Assuming the relationship goes through subject
            queryset = queryset.filter(subject__curriculum_id=curriculum_id)
        
        if year:
            queryset = queryset.filter(year=year)

        # If all parameters are provided, return filtered questions
        if subject_id and curriculum_id and year:
            serializer = PastQuestionSerializer(queryset, many=True)
            return Response(serializer.data)
        
        # If not all parameters are provided, return an empty list
        return Response([])

    def post(self, request):
        # Existing post method remains the same
        is_theory = request.data.get('is_theory', False)
        if is_theory: # Theory question
            required_fields = ['curriculum', 'subject', 'year', 'question']
        else: # MCQ
            required_fields = ['curriculum', 'subject', 'year', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option']
        
        missing_fields = [field for field in required_fields if not request.data.get(field)]
        
        if missing_fields:
            return Response({'error': f"Missing fields: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Serialize and save the question
        serializer = PastQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TopicsBySubjectAndCurriculumView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, curriculum_id, subject_id):
        topics = Topic.objects.filter(subject__curriculum_id=curriculum_id, subject_id=subject_id)
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)


class SubtopicsByTopicSubjectAndCurriculumView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, curriculum_id, subject_id, topic_id):
        subtopics = Subtopic.objects.filter(topic__subject__curriculum_id=curriculum_id, topic__subject_id=subject_id, topic_id=topic_id)
        serializer = SubtopicSerializer(subtopics, many=True)
        return Response(serializer.data)