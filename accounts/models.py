from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from datacollector.models import Subject, PastQuestion

class User(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Student')
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.username

class MockExam(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)
    start_time = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField()  # Duration in minutes
    status = models.CharField(max_length=50, default='ongoing')

    def __str__(self):
        return f"MockExam for {self.user.username}"

class MockExamQuestion(models.Model):
    mock_exam = models.ForeignKey(MockExam, on_delete=models.CASCADE)
    question = models.ForeignKey(PastQuestion, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=255, blank=True, null=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Exam Question: {self.question.question_text[:50]}..."

class UserPerformance(models.Model):
    EXAM_TYPE_CHOICES = [
        ('single_subject', 'Single Subject'),
        ('complete_mock', 'Complete Mock Exam'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='performances')
    subject = models.ForeignKey('datacollector.Subject', on_delete=models.CASCADE)
    topic = models.ForeignKey('datacollector.Topic', on_delete=models.CASCADE)
    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    time_spent = models.PositiveIntegerField(default=0)  # Time in seconds
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES, default='single_subject')

    @property
    def accuracy(self):
        if self.total_questions > 0:
            return (self.correct_answers / self.total_questions) * 100
        return 0

    @property
    def avg_time_per_question(self):
        if self.total_questions > 0:
            return self.time_spent / self.total_questions
        return 0
