# """
# Render-specific settings for Django IT Helpdesk application.
# Optimized for Render cloud platform deployment.
# """

# import os
# import dj_database_url
# from pathlib import Path

# # Bypass MariaDB version check for compatibility with MariaDB 10.4.32
# try:
#     import bypass_version_check
# except ImportError:
#     pass

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-this-in-production')

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# # Render handles host validation, but we'll be specific
# ALLOWED_HOSTS = [
#     '.onrender.com',  # Render subdomains
#     'superdoll.co.tz',
#     'www.superdoll.co.tz',
#     'localhost',
#     '127.0.0.1',
# ]

# # Add any additional hosts from environment
# if 'ALLOWED_HOSTS' in os.environ:
#     ALLOWED_HOSTS.extend(os.environ['ALLOWED_HOSTS'].split(','))

# # Application definition - Full Django features supported on Render
# INSTALLED_APPS = [
#     'daphne',  # Render supports WebSockets
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'channels',  # WebSocket support
#     'corsheaders',
#     'tickets',
# ]

# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'helpdesk.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'helpdesk.wsgi.application'
# ASGI_APPLICATION = 'helpdesk.asgi.application'

# # Database - Render provides PostgreSQL by default, but we can use MySQL too
# # Check if DATABASE_URL is provided (Render PostgreSQL)
# if 'DATABASE_URL' in os.environ:
#     DATABASES = {
#         'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
#     }
# else:
#     # Fallback to MySQL configuration
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': os.environ.get('DB_NAME', 'django_it_help'),
#             'USER': os.environ.get('DB_USER', 'root'),
#             'PASSWORD': os.environ.get('DB_PASSWORD', ''),
#             'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
#             'PORT': os.environ.get('DB_PORT', '3306'),
#             'OPTIONS': {
#                 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#                 'charset': 'utf8mb4',
#                 'use_unicode': True,
#             },
#             'TEST': {
#                 'CHARSET': 'utf8mb4',
#                 'COLLATION': 'utf8mb4_unicode_ci',
#             }
#         }
#     }

# # Channels configuration for WebSocket support
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
#         },
#     },
# }

# # Password validation
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#         'OPTIONS': {
#             'min_length': 8,
#         }
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

# # Internationalization
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# # Static files configuration for Render
# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATICFILES_DIRS = [
#     BASE_DIR / 'static',
# ]

# # Static files storage with compression
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# # Media files configuration
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# # Default primary key field type
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # CORS settings - More restrictive for production
# CORS_ALLOW_ALL_ORIGINS = False
# CORS_ALLOWED_ORIGINS = [
#     "https://superdoll.co.tz",
#     "https://www.superdoll.co.tz",
# ]

# # Allow CORS for Render deployments
# CORS_ALLOWED_ORIGIN_REGEXES = [
#     r"^https://.*\.onrender\.com$",
# ]

# # Login URLs
# LOGIN_URL = '/login/'
# LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = '/login/'

# # Security Settings for Production
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = 'DENY'

# # HTTPS Settings for Render (Render handles SSL)
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = not DEBUG
# SESSION_COOKIE_SECURE = not DEBUG
# CSRF_COOKIE_SECURE = not DEBUG
# SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
# SECURE_HSTS_PRELOAD = not DEBUG

# # Session Security
# SESSION_COOKIE_AGE = 3600  # 1 hour
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_COOKIE_HTTPONLY = True

# # Email Configuration
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
# EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
# DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@superdoll.co.tz')

# # Logging Configuration for Render
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'INFO',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#         'level': 'INFO',
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'INFO',
#             'propagate': False,
#         },
#     },
# }

# # Cache Configuration - Use Redis if available
# if 'REDIS_URL' in os.environ:
#     CACHES = {
#         'default': {
#             'BACKEND': 'django_redis.cache.RedisCache',
#             'LOCATION': os.environ.get('REDIS_URL'),
#             'OPTIONS': {
#                 'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             }
#         }
#     }
# else:
#     # Fallback to database cache
#     CACHES = {
#         'default': {
#             'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#             'LOCATION': 'django_cache_table',
#         }
#     }

# # File upload settings
# FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
# DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
