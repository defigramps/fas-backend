from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    RegisterView,
    EmailVerificationView,
    LoginView,
    LogoutView,
    PasswordResetRequestView,
    PasswordResetView,
    UserViewSet,
    PerformanceReportView,
    AdminRoleView,
    UserProfileView,
    CumulativePerformanceView,
    InsightsView,
    RecommendationsView,
    MockExamInitView,
    MockExamQuestionsView,
    MockExamSubmitView,
    ResendOTPView,
    GoogleLogin,
)

# Initialize the DefaultRouter
router = DefaultRouter()
router.register(r'users', UserViewSet)

# Combine all URL patterns
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verification/', EmailVerificationView.as_view(), name='email-verification'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('login/', LoginView.as_view(), name='login'),
    path('google-login/', GoogleLogin.as_view(), name='google-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('admin/roles/', AdminRoleView.as_view(), name='admin-roles'),

    # Mock Exams API
    path('mock-exams/init/', MockExamInitView.as_view(), name='mock_exam_init'),
    path('mock-exams/<int:mock_exam_id>/questions/', MockExamQuestionsView.as_view(), name='mock_exam_questions'),
    path('mock-exams/<int:mock_exam_id>/submit/', MockExamSubmitView.as_view(), name='mock_exam_submit'),

    # Performance API
    path('performance/cumulative/', CumulativePerformanceView.as_view(), name='cumulative_performance'),
    path('performance/insights/', InsightsView.as_view(), name='insights'),
    path('performance/report/', PerformanceReportView.as_view(), name='performance_report'),
    path('performance/recommendations/', RecommendationsView.as_view(), name='recommendations'),

    # Include router URLs for UserViewSet
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)