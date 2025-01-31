import os
from pathlib import Path
import environ
import dj_database_url

# Initialize environment variables from the .env file
env = environ.Env()
environ.Env.read_env(os.path.join(Path(__file__).resolve().parent.parent, '.env'))

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

    # Your apps
    'accounts',
    'datacollector',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

# Redirect URLs
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'accounts.User'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins (adjust for production)
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",  # Add your frontend URL here
#     "http://127.0.0.1:5173",
# ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Add this line
]

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = '8b6088e8d8055d'
EMAIL_HOST_PASSWORD = '3eac09a4e694df'
EMAIL_PORT = '2525' 


# Static files (CSS, JavaScript, images)
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DATABASES = {
    'default': env.db(),  # Will pull from DATABASE_URL in the .env
}


# DATABASES['default'] = dj_database_url.parse("postgresql://rheons_dc_user:LshjGGPoe4PndoD1M4MNr3IFr5Rs6TW2@dpg-ctg3tp1opnds73dku6bg-a.oregon-postgres.render.com/rheons_dc")

SECRET_KEY = env('SECRET_KEY')  # Secure your secret key with .env

# Social Authentication Settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': env('SOCIAL_AUTH_GOOGLE_CLIENT_ID'),
            'secret': env('SOCIAL_AUTH_GOOGLE_SECRET'),
            'key': ''
        }
    },
    'facebook': {
        'APP': {
            'client_id': env('SOCIAL_AUTH_FACEBOOK_KEY'),
            'secret': env('SOCIAL_AUTH_FACEBOOK_SECRET'),
            'key': ''
        }
    }
}

# TEMPLATES settings for Django Admin
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'allauth.account.context_processors.account',
                'allauth.socialaccount.context_processors.socialaccount',
            ],
        },
    },
]

ALLOWED_HOSTS = ['*']
ROOT_URLCONF = 'rheons.urls'
DEBUG = env.bool('DEBUG', default=True)

REST_KNOX = {
    'TOKEN_TTL': None,
    'AUTO_REFRESH': True,
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'