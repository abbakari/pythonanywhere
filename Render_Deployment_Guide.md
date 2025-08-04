# Deploy Django IT Helpdesk to Render

## 🌟 Why Render?
- ✅ **Better Django support** than Vercel
- ✅ **WebSocket support** (Django Channels work!)
- ✅ **Persistent storage**
- ✅ **Automatic SSL certificates**
- ✅ **Custom domain support** (superdoll.co.tz)
- ✅ **PostgreSQL database included**
- ✅ **Background workers support**
- ✅ **Free tier available**

## 📋 Prerequisites
- GitHub account
- Render account (free at https://render.com)
- Your Django project ready

## 🔧 Step 1: Prepare Your Django Project for Render

### Create Render Configuration Files:

**1. Create `render.yaml`:**
```yaml
databases:
  - name: django-it-helpdesk-db
    databaseName: django_it_help
    user: django_user

services:
  - type: web
    name: django-it-helpdesk
    env: python
    buildCommand: "./build.sh"
    startCommand: "gunicorn helpdesk.wsgi:application"
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: django-it-helpdesk-db
          property: connectionString
      - key: DJANGO_SETTINGS_MODULE
        value: helpdesk.settings_render
      - key: PYTHON_VERSION
        value: 3.11.0
```

**2. Create `build.sh`:**
```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements_render.txt

# Bypass MariaDB version check
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings_render')
django.setup()
"

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
```

**3. Create `requirements_render.txt`:**
```txt
Django>=5.0,<6.0
psycopg2-binary>=2.9.0
daphne>=4.0.0
channels>=4.0.0
channels-redis>=4.0.0
django-cors-headers>=4.0.0
python-decouple>=3.8
whitenoise>=6.5.0
gunicorn>=21.0.0
redis>=4.5.0
```

**4. Create Render-specific settings `helpdesk/settings_render.py`:**
```python
from .settings_production import *
import os
import dj_database_url

# Render-specific settings
DEBUG = False

# Parse database URL from Render
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# Update database settings for PostgreSQL
DATABASES['default'].update({
    'OPTIONS': {
        'charset': 'utf8',
    }
})

# Allowed hosts for Render
ALLOWED_HOSTS = [
    'django-it-helpdesk.onrender.com',  # Your Render URL
    'superdoll.co.tz',
    'www.superdoll.co.tz',
    'localhost',
    '127.0.0.1'
]

# Static files configuration for Render
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Redis configuration for Channels (Render provides Redis)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379'),
    }
}

# Security settings for production
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
```

**5. Update `requirements_render.txt` to include database URL parser:**
```txt
Django>=5.0,<6.0
psycopg2-binary>=2.9.0
dj-database-url>=2.0.0
daphne>=4.0.0
channels>=4.0.0
channels-redis>=4.0.0
django-cors-headers>=4.0.0
python-decouple>=3.8
whitenoise>=6.5.0
gunicorn>=21.0.0
redis>=4.5.0
```

## 🚀 Step 2: Deploy to Render

### 1. Push to GitHub:
```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Prepare for Render deployment"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/django-it-helpdesk.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Render:
1. Go to https://render.com and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name:** `django-it-helpdesk`
   - **Environment:** `Python`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn helpdesk.wsgi:application`
   - **Instance Type:** Free (or paid for better performance)

### 3. Configure Environment Variables:
In the Render dashboard, add these environment variables:
```
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=helpdesk.settings_render
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=abbakariamali@gmail.com
EMAIL_HOST_PASSWORD=fjikqzmjqcfqhhfc
DEFAULT_FROM_EMAIL=superdoll.co.tz
PYTHON_VERSION=3.11.0
```

### 4. Create PostgreSQL Database:
1. In Render dashboard → **"New +"** → **"PostgreSQL"**
2. **Name:** `django-it-helpdesk-db`
3. **Database Name:** `django_it_help`
4. **User:** `django_user`
5. The `DATABASE_URL` will be automatically provided to your web service

### 5. Create Redis Instance (for Channels):
1. **"New +"** → **"Redis"**
2. **Name:** `django-it-helpdesk-redis`
3. The `REDIS_URL` will be automatically provided

### 6. Add Custom Domain:
1. In your web service → **"Settings"** → **"Custom Domains"**
2. Add `superdoll.co.tz` and `www.superdoll.co.tz`
3. Configure DNS records as shown by Render
4. SSL certificate will be automatically generated

## 🔄 Step 3: Database Migration

Since you're moving from MySQL to PostgreSQL, you'll need to migrate your data:

### Option A: Fresh Start (Recommended)
1. Let Render create fresh database tables
2. Create a new superuser:
   ```bash
   # In Render shell
   python manage.py createsuperuser
   ```

### Option B: Data Migration
1. Export data from MySQL:
   ```bash
   python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > data.json
   ```
2. Upload `data.json` to your repository
3. Load data in Render:
   ```bash
   python manage.py loaddata data.json
   ```

## 📊 Render Services Architecture:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Service   │    │   PostgreSQL     │    │     Redis       │
│   (Django App)  │◄──►│   (Database)     │    │   (Channels)    │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐
│  Custom Domain  │
│ superdoll.co.tz │
└─────────────────┘
```

## 💰 Pricing Comparison:

### Free Tier:
- **Web Service:** Free (with limitations)
- **PostgreSQL:** Free (1GB storage)
- **Redis:** Free (25MB)
- **Custom Domain:** Free
- **SSL Certificate:** Free

### Paid Tier (Recommended for Production):
- **Web Service:** $7/month (better performance)
- **PostgreSQL:** $7/month (more storage)
- **Redis:** $5/month (more memory)

## 🎉 Benefits of Render:

### ✅ Django-Friendly:
- Full Django support including Channels
- PostgreSQL database included
- Redis for caching and WebSockets
- Background workers support

### ✅ Production-Ready:
- Automatic SSL certificates
- Custom domain support
- Health checks and auto-restart
- Horizontal scaling available

### ✅ Developer Experience:
- Git-based deployments
- Environment variable management
- Built-in monitoring
- Shell access for debugging

## 🔧 Post-Deployment Steps:

1. **Create Superuser:**
   ```bash
   # In Render shell
   python manage.py createsuperuser
   ```

2. **Test Your Application:**
   - Visit your Render URL
   - Test admin panel
   - Test WebSocket features (if using Channels)

3. **Configure Custom Domain:**
   - Add DNS records
   - Test SSL certificate

4. **Set up Monitoring:**
   - Enable Render's built-in monitoring
   - Set up email alerts

## 🚨 Important Notes:

- **Database Change:** Moving from MySQL to PostgreSQL
- **WebSocket Support:** Full Django Channels support
- **File Storage:** Consider using AWS S3 for media files in production
- **Email:** Your Gmail SMTP configuration will work perfectly

Render is highly recommended for Django applications because it provides better support for Django-specific features compared to Vercel!
