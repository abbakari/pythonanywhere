"""
Vercel-specific settings for Django IT Helpdesk application.
Optimized for serverless deployment on Vercel platform.
"""

import os
from pathlib import Path

# Bypass MariaDB version check for compatibility with MariaDB 10.4.32
try:
    import bypass_version_check
except ImportError:
    pass

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Vercel handles host validation, but we'll be specific
ALLOWED_HOSTS = [
    '.vercel.app',  # Vercel subdomains
    'superdoll.co.tz',
    'www.superdoll.co.tz',
    'localhost',
    '127.0.0.1',
]

# Application definition - Optimized for Vercel serverless
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'tickets',
    # Note: Removed 'daphne' and 'channels' as they don't work well with Vercel serverless
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'helpdesk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'helpdesk.wsgi.application'

# Database - Use environment variables for cloud database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'django_it_help'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
        'TEST': {
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4_unicode_ci',
        }
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files configuration for Vercel
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles_build' / 'static'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Static files storage with compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings - More restrictive for production
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://superdoll.co.tz",
    "https://www.superdoll.co.tz",
]

# Allow CORS for Vercel preview deployments
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.vercel\.app$",
]

# Login URLs
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Security Settings for Production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS Settings for Vercel (Vercel handles SSL)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Session Security
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_HTTPONLY = True

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@superdoll.co.tz')

# Logging Configuration for Vercel
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Cache Configuration (using database cache for serverless)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache_table',
    }
}

# Vercel-specific optimizations
# Disable migrations check in production (Vercel builds are stateless)
MIGRATION_MODULES = {}

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
