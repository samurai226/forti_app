# chat_api/settings.py

import os
import dj_database_url
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-prod-k8m2n9p4q7w1e3r5t6y8u0i2o4p6a8s1d3f5g7h9j1k3l5m7n9')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    # DISABLED: SECURE_SSL_REDIRECT to prevent redirect loops in mobile apps
    # SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'
else:
    # Development settings - allow HTTP
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    APPEND_SLASH = False  # Disable automatic slash appending for development

# Dynamic ALLOWED_HOSTS based on environment
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '10.0.2.2',  # Android emulator can reach host machine via 10.0.2.2
    'testserver',  # For Django test client
    'forti-app.onrender.com',
    '.onrender.com',  # Render deployment
    '.herokuapp.com',  # Heroku deployment
    '.vercel.app',     # Vercel deployment
    '.railway.app',    # Railway deployment
]

# Add additional hosts from environment variable
if os.getenv('ALLOWED_HOSTS'):
    ALLOWED_HOSTS.extend(os.getenv('ALLOWED_HOSTS').split(','))

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Applications tierces
    'rest_framework',
    'corsheaders',
    'channels',
    'storages',
    
    # Applications personnalisées (re-enabled after fixing CORS)
    'accounts',
    'conversations.apps.ConversationsConfig',  # Re-enabled for WebSocket functionality
    'matching',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chat_api.urls'

# ASGI Application for WebSocket support
ASGI_APPLICATION = 'chat_api.asgi.application'
WSGI_APPLICATION = 'chat_api.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'chat_api.wsgi.application'

# Base de données
# Database: Use Postgres when DATABASE_URL is set (e.g., on Render),
# otherwise fall back to local SQLite for development.
DATABASE_URL = os.getenv('DATABASE_URL', '').strip()

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Modèle utilisateur personnalisé (re-enabled with accounts app)
AUTH_USER_MODEL = 'accounts.User'

# Configuration des backends d'authentification
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Backend Django par défaut
]

# Configuration de REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Configuration de Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# Configuration CORS
CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins for mobile app compatibility

# CORS allowed origins - dynamic based on environment
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000",
    "http://localhost:8080",  # Vue dev server
    "http://127.0.0.1:8080",
    "https://forti-app.onrender.com",  # Render deployment
    # Add mobile app origins
    "capacitor://localhost",  # Capacitor development
    "ionic://localhost",      # Ionic development
    "http://localhost",       # Local development
    "http://10.0.2.2",        # Android emulator
    "http://10.0.3.2",        # Genymotion emulator
    # Flutter mobile app origins - FIXED: Added proper schemes
    "file://localhost",       # Flutter file:// protocol
    "app://localhost",        # Flutter app:// protocol
    "flutter://localhost",    # Flutter flutter:// protocol
    # Additional Flutter origins
    "http://localhost:3000",  # Flutter web development
    "https://localhost:3000", # Flutter web HTTPS
    "http://127.0.0.1:3000",  # Flutter web localhost
    "https://127.0.0.1:3000", # Flutter web localhost HTTPS
]

# Additional CORS settings for mobile apps
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_HEADERS = True
CORS_ALLOW_ALL_METHODS = True

# Add additional CORS origins from environment
if os.getenv('CORS_ALLOWED_ORIGINS'):
    CORS_ALLOWED_ORIGINS.extend(os.getenv('CORS_ALLOWED_ORIGINS').split(','))

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-appwrite-project',  # For Appwrite integration
    'x-appwrite-key',      # For Appwrite integration
]

# CORS preflight max age
CORS_PREFLIGHT_MAX_AGE = 86400  # 24 hours

# Additional settings to prevent redirect loops in mobile apps
USE_TZ = True
TIME_ZONE = 'UTC'

# Disable automatic trailing slash redirects that can cause issues
APPEND_SLASH = False

# Note: MIDDLEWARE is already defined above

# Configuration du cache
# Use Redis in production, local memory in development
if os.getenv('REDIS_URL'):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': os.getenv('REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

# Configuration des channels (WebSocket)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.getenv('REDIS_URL', 'redis://localhost:6379')],
            "capacity": 1500,
            "expiry": 60,
        },
    },
}

# Fallback to in-memory layer if Redis is not available
if not os.getenv('REDIS_URL'):
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }

# CloudFront CDN Configuration
CLOUDFRONT_DISTRIBUTION_ID = os.getenv('CLOUDFRONT_DISTRIBUTION_ID')
CLOUDFRONT_DOMAIN = os.getenv('CLOUDFRONT_DOMAIN', 'd2czzsmpeluuz5.cloudfront.net')

# Firebase Cloud Messaging Configuration
FCM_SERVER_KEY = os.environ.get('FCM_SERVER_KEY', '')
FCM_PROJECT_ID = os.environ.get('FCM_PROJECT_ID', '')

# AWS S3 Configuration for CloudFront
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', 'fortu-app-assets-dev')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-west-2')
AWS_S3_CUSTOM_DOMAIN = CLOUDFRONT_DOMAIN
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',  # 24 hours default
}
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False

# Static and Media files with CloudFront
if CLOUDFRONT_DOMAIN:
    STATIC_URL = f'https://{CLOUDFRONT_DOMAIN}/static/'
    MEDIA_URL = f'https://{CLOUDFRONT_DOMAIN}/media/'
    
    # Use S3 for file storage
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
else:
    # Fallback to local storage
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

# Configuration Appwrite (removed)
# APPWRITE_CONFIG = {
#     'ENDPOINT': 'https://your-appwrite-endpoint.com/v1',
#     'PROJECT_ID': 'your-project-id',
#     'API_KEY': 'your-api-key',
#     'WEBHOOK_SECRET': 'your-webhook-secret',
# }

# Configuration des logs (simplified)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Fichiers statiques (CSS, JavaScript, Images) - removed duplicate
# STATIC_URL = '/static/'  # Already defined above
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Static files finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Static files storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# AWS S3 Configuration (removed duplicate - already defined above)
# AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-west-2')
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
# AWS_DEFAULT_ACL = None
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
# AWS_S3_FILE_OVERWRITE = False
# AWS_S3_VERIFY = True

# Media files - Use S3 if configured, otherwise local (simplified)
if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME:
    # Use S3 for media files
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    MEDIA_ROOT = ''
else:
    # Fallback to local storage
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Session configuration
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Email configuration (for future use)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

# Rate limiting (for future use)
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'

# API configuration
API_VERSION = 'v1'
API_PAGE_SIZE = 20
API_MAX_PAGE_SIZE = 100

# Appwrite configuration (if needed)
APPWRITE_ENDPOINT = os.getenv('APPWRITE_ENDPOINT', '')
APPWRITE_PROJECT_ID = os.getenv('APPWRITE_PROJECT_ID', '')
APPWRITE_API_KEY = os.getenv('APPWRITE_API_KEY', '')
APPWRITE_WEBHOOK_SECRET = os.getenv('APPWRITE_WEBHOOK_SECRET', '')

# Health check configuration
HEALTH_CHECK = {
    'DISK_USAGE_MAX': 90,  # percent
    'MEMORY_MIN': 100,     # in MB
}

# Performance settings
CONN_MAX_AGE = 60  # Database connection pooling
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
