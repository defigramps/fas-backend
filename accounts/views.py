import logging
import base64
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from .serializers import RegisterSerializer, UserSerializer
from .models import User
from .permissions import IsAdmin, IsStudent
from rest_framework import viewsets
from rest_framework.decorators import action
from datacollector.models import  PastQuestion, Subject
from .models import MockExam, MockExamQuestion
from .serializers import MockExamSerializer, MockExamQuestionSerializer
from datacollector.serializers import PastQuestionSerializer, SubjectSerializer
import random
from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import Avg, Sum, F, ExpressionWrapper, FloatField
from datacollector.models import Topic
from .models import UserPerformance
from .serializers import UserPerformanceSerializer
from .serializers import UserProfileSerializer
from django.core.cache import cache
from google.oauth2 import id_token
from smtplib import SMTPException
# from google.auth.transport import requests
import requests as http_requests  # Add this at the top with your other imports
from google.auth.transport import requests as google_requests 

User = get_user_model()

# Initialize logger
logger = logging.getLogger(__name__)

# Helper to generate secure UID
def generate_uidb64(email):
    return base64.urlsafe_b64encode(email.encode()).decode()

# Helper to generate secure tokens
def generate_email_token(user):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(user.email, salt="email-verification")

# Helper to verify secure tokens
def verify_email_token(token, max_age=3600):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(token, salt="email-verification", max_age=max_age)
        return email
    except Exception:
        return None

# Helper to send email verification
def send_verification_email(user):
    try:
        token = generate_email_token(user)
        uidb64 = generate_uidb64(user.email)
        verification_url = f"http://127.0.0.1:8000/api/accounts/email-verification/{uidb64}/{token}/"
        send_mail(
            subject="Email Verification for Your Account",
            message=f"Click the link below to verify your email:\n{verification_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Failed to send verification email to {user.email}: {str(e)}")
        raise

# Helper to generate 6-digit OTP
def generate_otp():
    return random.randint(100000, 999999)

# Helper to send OTP email
def send_otp_email(user, otp):
    try:
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
    except SMTPException as e:
        print(f"Failed to send OTP email to {user.email}: {e}")
        # Handle the error appropriately, e.g., log it or notify the user

# Registration view
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        user.is_active = False  # Make the user inactive until email verification
        user.save()

        otp = generate_otp()
        cache.set(f'email_verification_otp_{user.email}', otp, timeout=600)  # OTP valid for 10 minutes
        send_otp_email(user, otp)

        return Response(
            {"message": "User registered successfully. Check your email for OTP."},
            status=status.HTTP_201_CREATED,
        )

# Email verification view
class EmailVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        cached_otp = cache.get(f'email_verification_otp_{email}')
        if cached_otp is None or str(cached_otp) != str(otp):
            return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user.is_active = True
        user.save()
        cache.delete(f'email_verification_otp_{email}')

        return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)

# Login view
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=user.username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)
        
class GoogleLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')

        if not token:
            return Response({"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify the Google token
            idinfo = id_token.verify_oauth2_token(
                token, 
                google_requests.Request(), 
                '139684706482-2eklvi835coms7en6m7loudfh5370tor.apps.googleusercontent.com'
            )

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # Extract email and generate UID and token
            email = idinfo['email']
            uidb64 = generate_uidb64(email)

            # Check if the user exists
            user = User.objects.filter(email=email).first()
            if not user:
                # If user does not exist, create a new user (optional)
                user = User.objects.create(
                    email=email,
                    username=email.split('@')[0],
                    is_active=True  # Activate user immediately for Google login
                )

            # Generate a secure token for the user
            email_token = generate_email_token(user)

            return Response(
                {
                    "uid": uidb64,
                    "token": email_token,
                    "email": email
                },
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            logger.error(f"Google token verification failed: {str(e)}")
            return Response({"error": "Invalid Google token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"An unexpected error occurred during Google login: {str(e)}")
            return Response({"error": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        otp = generate_otp()
        cache.set(f'password_reset_otp_{email}', otp, timeout=600)  # OTP valid for 10 minutes
        send_otp_email(user, otp)

        return Response({"message": "Password reset OTP sent."}, status=status.HTTP_200_OK)

# Password reset view
class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('password')

        if not email or not otp or not new_password:
            return Response({"error": "Email, OTP, and new password are required."}, status=status.HTTP_400_BAD_REQUEST)

        cached_otp = cache.get(f'password_reset_otp_{email}')
        if cached_otp is None or str(cached_otp) != str(otp):
            return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(new_password)
        user.save()
        cache.delete(f'password_reset_otp_{email}')

        return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)

# Logout view
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Ensure token is provided
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            logger.error("Authorization header is missing")
            return Response({"error": "Authorization header is required."}, status=status.HTTP_401_UNAUTHORIZED)

        # Extract token from the header
        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) == 2 else None
        if not token:
            logger.error("Token is missing in the Authorization header")
            return Response({"error": "Token is required."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Try to retrieve the token from the database
            token_obj = Token.objects.get(key=token)
            logger.debug(f"Token found: {token_obj.key}")
            # Delete the token to log out
            token_obj.delete()
            logger.debug(f"User logged out: {request.user.username}")
            return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            logger.error(f"Invalid token: {token}")
            return Response({"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(f"Error during logout: {str(e)}")
            return Response({"error": "Logout failed."}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['get'], permission_classes=[IsAdmin])
    def students(self, request):
        students = User.objects.filter(role="Student")
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)
class AdminRoleView(APIView):
    def post(self, request):
        # Your logic for handling the role assignment
        return Response({"message": "Roles assigned successfully."}, status=status.HTTP_200_OK)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MockExamInitView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        subjects = request.data.get('subjects', [])
        duration = request.data.get('duration', 30)

        if not subjects:
            return Response({"error": "Subjects are required."}, status=status.HTTP_400_BAD_REQUEST)

        mock_exam = MockExam.objects.create(user=user, duration=duration)
        mock_exam.subjects.add(*Subject.objects.filter(id__in=subjects))
        mock_exam.save()

        questions = []
        for subject in mock_exam.subjects.all():
            # Fetch questions directly from your database instead of making an HTTP request
            subject_questions = PastQuestion.objects.filter(
                curriculum=1,
                subject=subject
            ).values()
            
            # Convert queryset to list for random sampling
            subject_questions = list(subject_questions)
            
            if subject.name == 'Use of English':
                selected_questions = random.sample(subject_questions, min(len(subject_questions), 60))
            else:
                selected_questions = random.sample(subject_questions, min(len(subject_questions), 40))
            
            questions.extend(selected_questions)

        random.shuffle(questions)

        # Create MockExamQuestion objects and fetch them with all related data
        mock_exam_questions = []
        for question in questions:
            mock_exam_question = MockExamQuestion.objects.create(
                mock_exam=mock_exam,
                question_id=question['id']
            )
            mock_exam_questions.append(mock_exam_question)

        # Use select_related to fetch related question data efficiently
        questions_with_data = MockExamQuestion.objects.filter(
            mock_exam=mock_exam
        ).select_related('question')

        serialized_questions = MockExamQuestionSerializer(questions_with_data, many=True).data

        return Response({
            "mock_exam": MockExamSerializer(mock_exam).data,
            "questions": serialized_questions
        }, status=status.HTTP_201_CREATED)


class MockExamQuestionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, mock_exam_id):
        try:
            mock_exam = MockExam.objects.get(id=mock_exam_id, user=request.user)
            questions = MockExamQuestion.objects.filter(mock_exam=mock_exam)
            return Response(MockExamQuestionSerializer(questions, many=True).data, status=status.HTTP_200_OK)
        except MockExam.DoesNotExist:
            return Response({"error": "Mock exam not found."}, status=status.HTTP_404_NOT_FOUND)
        
class MockExamSubmitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, mock_exam_id):
        try:
            mock_exam = MockExam.objects.get(id=mock_exam_id, user=request.user)

            # Validate exam completion time
            if timezone.now() > mock_exam.start_time + timedelta(minutes=mock_exam.duration):
                return Response({"error": "Exam time has expired."}, status=status.HTTP_400_BAD_REQUEST)

            # Get answers from the request
            submitted_answers = request.data.get('answers', [])
            if not submitted_answers:
                return Response({"error": "No answers provided."}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve all questions for the mock exam
            mock_exam_questions = MockExamQuestion.objects.filter(mock_exam=mock_exam)
            total_questions = mock_exam_questions.count()
            score = 0
            detailed_results = []

            # Build a dictionary of submitted answers for easy lookup
            submitted_answers_dict = {
                answer['question_id']: answer.get('user_answer') for answer in submitted_answers
            }

            # Initialize subject scores
            subject_scores = {subject.id: {'correct': 0, 'total': 0} for subject in mock_exam.subjects.all()}

            # Process each question in the mock exam
            for mock_question in mock_exam_questions:
                question = mock_question.question
                user_answer = submitted_answers_dict.get(mock_question.id)

                # Mark as incorrect if unanswered or if the answer is wrong
                is_correct = user_answer == question.correct_option if user_answer else False
                mock_question.user_answer = user_answer
                mock_question.is_correct = is_correct
                mock_question.save()

                # Update subject scores
                subject_scores[question.subject.id]['total'] += 1
                if is_correct:
                    subject_scores[question.subject.id]['correct'] += 1

                detailed_results.append({
                    "question_id": question.id,
                    "question": question.question,
                    "correct_option": question.correct_option,
                    "user_answer": user_answer,
                    "is_correct": is_correct,
                    "explanation": question.explanation,
                })

            # Mark the mock exam as completed
            mock_exam.status = 'completed'
            mock_exam.save()

            # Calculate total score for complete mock exams
            total_score = 0
            for subject_id, scores in subject_scores.items():
                if scores['total'] > 0:
                    subject_score = (scores['correct'] / scores['total']) * 100
                    total_score += subject_score

            # Determine the remark based on the total score
            if total_score >= 360:
                remark = "Excellent"
            elif total_score >= 320:
                remark = "Very Good"
            elif total_score >= 280:
                remark = "Good"
            elif total_score >= 240:
                remark = "Average"
            elif total_score >= 200:
                remark = "Below Average"
            elif total_score >= 160:
                remark = "Poor"
            else:
                remark = "Very Poor"

            return Response({
                "score": total_score,
                "remark": remark,
                "total_questions": total_questions,
                "results": detailed_results,
            }, status=status.HTTP_200_OK)

        except MockExam.DoesNotExist:
            return Response({"error": "Mock exam not found."}, status=status.HTTP_404_NOT_FOUND)


        
class CumulativePerformanceView(APIView):
    def get(self, request):
        user = request.user
        
        # Step 1: Annotate the accuracy for each record
        performance_data = UserPerformance.objects.filter(user=user).values('subject__name').annotate(
            total_questions=Sum('total_questions'),
            correct_answers=Sum('correct_answers'),
            time_spent=Sum('time_spent'),
            accuracy=ExpressionWrapper(
                F('correct_answers') * 100.0 / F('total_questions'),
                output_field=FloatField()
            )
        )
        
        # Step 2: Calculate the average accuracy
        average_accuracy = performance_data.aggregate(
            avg_accuracy=Avg('accuracy')
        )

        # Combine both the performance data and the calculated average accuracy
        performance_data = list(performance_data)  # Convert queryset to list to combine
        performance_data.append({'avg_accuracy': average_accuracy['avg_accuracy']})
        
        return Response(performance_data, status=status.HTTP_200_OK)
    
class InsightsView(APIView):
    def get(self, request):
        user = request.user
        total_time = UserPerformance.objects.filter(user=user).aggregate(total_time=Sum('time_spent'))['total_time'] or 0
        accuracy = UserPerformance.objects.filter(user=user).aggregate(average_accuracy=Avg(F('correct_answers') * 100.0 / F('total_questions')))['average_accuracy'] or 0
        speed = UserPerformance.objects.filter(user=user).aggregate(average_speed=Avg(F('time_spent') / F('total_questions')))['average_speed'] or 0

        insights = {
            "time_spent": total_time,
            "accuracy": accuracy,
            "speed": speed,
        }
        return Response(insights, status=status.HTTP_200_OK)

class RecommendationsView(APIView):
    def get(self, request):
        user = request.user
        
        # Calculate accuracy using an ExpressionWrapper
        weak_areas = UserPerformance.objects.filter(
            user=user,
            correct_answers__lt=F('total_questions') * 0.5
        ).annotate(
            accuracy=ExpressionWrapper(
                F('correct_answers') / F('total_questions'),
                output_field=FloatField()
            ),
            total_time_spent=Sum('time_spent')  # Rename to avoid conflict
        ).values('subject__name', 'topic__name', 'accuracy', 'total_time_spent').order_by('accuracy')

        # If there are no weak areas, return a meaningful response
        if not weak_areas.exists():
            return Response({"message": "No weak areas found."}, status=status.HTTP_200_OK)
        
        return Response(weak_areas, status=status.HTTP_200_OK)

class PerformanceReportView(APIView):
    def get(self, request):
        user = request.user
        
        # Calculate performance data
        performance_data = UserPerformance.objects.filter(user=user).values('subject__name', 'topic__name', 'exam_type').annotate(
            total_questions=Sum('total_questions'),
            correct_answers=Sum('correct_answers'),
            time_spent=Sum('time_spent'),
            accuracy=ExpressionWrapper(
                F('correct_answers') * 100.0 / F('total_questions'),
                output_field=FloatField()
            ),
            avg_time_per_question=ExpressionWrapper(
                F('time_spent') / F('total_questions'),
                output_field=FloatField()
            )
        )

        # Identify strengths and weaknesses
        strengths = performance_data.filter(accuracy__gt=80)
        weaknesses = performance_data.filter(accuracy__lt=50)

        # Recommendations
        recommendations = []
        for weakness in weaknesses:
            recommendations.append(f"Revisit topic {weakness['topic__name']} in subject {weakness['subject__name']}.")

        # Calculate total score for complete mock exam
        complete_mock_data = performance_data.filter(exam_type='complete_mock')
        total_score = 0
        for data in complete_mock_data:
            if data['subject__name'] == 'Use of English':
                total_score += data['correct_answers'] * (400 / 240)  # 60 questions
            else:
                total_score += data['correct_answers'] * (400 / 120)  # 40 questions

        report = {
            "performance_data": performance_data,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "total_score": total_score
        }

        return Response(report, status=status.HTTP_200_OK)

class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        otp = generate_otp()
        cache.set(f'email_verification_otp_{email}', otp, timeout=600)  # OTP valid for 10 minutes
        send_otp_email(user, otp)

        return Response({"message": "OTP resent successfully."}, status=status.HTTP_200_OK)