from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="RHEONS API",
        default_version='v1',
        description="""
        This is the API documentation for My Django Application.

        ## Overview
        This API provides endpoints for user authentication, mock exams, and performance tracking.

        ## Authentication
        - **Register**: Create a new user account.
        - **Email Verification**: Verify user email addresses.
        - **Password Reset**: Request and reset passwords.
        - **Login/Logout**: User login and logout.

        ## Mock Exams
        - **Initialize Mock Exam**: Start a new mock exam.
        - **Get Questions**: Retrieve questions for a specific mock exam.
        - **Submit Answers**: Submit answers for a mock exam.

        ## Performance
        - **Cumulative Performance**: Get cumulative performance data.
        - **Insights**: Get performance insights.
        - **Recommendations**: Get performance improvement recommendations.

        ## Admin
        - **Roles Management**: Manage user roles.

        ## Data Collection
        - **Data Collection Endpoints**: Collect and manage data.

        ## Usage
        Each endpoint is documented with the required parameters and expected responses. Use the Swagger UI or Redoc to explore and test the endpoints interactively.
        """,
        # terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="tomudoh258@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),  # Include accounts app URLs with the correct prefix
    path('api/datacollector/', include('datacollector.urls')),  # Include datacollector app URLs with the correct prefix
    path('accounts/', include('allauth.urls')),  # Include allauth URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]