# Deploy Django IT Helpdesk to Vercel

## 🌟 Why Vercel?
- ✅ **Free tier available**
- ✅ **Automatic SSL certificates**
- ✅ **Custom domain support** (superdoll.co.tz)
- ✅ **Global CDN**
- ✅ **Automatic deployments from Git**
- ✅ **Serverless functions**

## 📋 Prerequisites
- GitHub account
- Vercel account (free at https://vercel.com)
- Your Django project ready

## 🔧 Step 1: Prepare Your Django Project for Vercel

### Create Vercel Configuration Files:

**1. Create `vercel.json`:**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "helpdesk/wsgi.py",
      "use": "@vercel/python",
      "config": { "maxLambdaSize": "15mb", "runtime": "python3.11" }
    },
    {
      "src": "build_files.sh",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "staticfiles_build"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/media/(.*)",
      "dest": "/media/$1"
    },
    {
      "src": "/(.*)",
      "dest": "helpdesk/wsgi.py"
    }
  ]
}
```

**2. Create `build_files.sh`:**
```bash
#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput --clear

# Create staticfiles_build directory for Vercel
mkdir -p staticfiles_build
cp -r staticfiles/* staticfiles_build/
```

**3. Create `requirements.txt` (if not exists):**
```txt
Django>=5.0,<6.0
mysqlclient>=2.2.0
daphne>=4.0.0
channels>=4.0.0
django-cors-headers>=4.0.0
python-decouple>=3.8
whitenoise>=6.5.0
gunicorn>=21.0.0
```

**4. Update `helpdesk/wsgi.py` for Vercel:**
```python
import os
from django.core.wsgi import get_wsgi_application

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings_production')

application = get_wsgi_application()

# Vercel serverless function handler
app = application
```

**5. Create Vercel-specific settings `helpdesk/settings_vercel.py`:**
```python
from .settings_production import *
import os

# Vercel-specific settings
DEBUG = False
ALLOWED_HOSTS = ['*']  # Vercel handles this

# Database - Use environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}

# Static files for Vercel
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Disable channels for serverless
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'channels']
if 'daphne' in INSTALLED_APPS:
    INSTALLED_APPS.remove('daphne')

# Remove ASGI application
ASGI_APPLICATION = None
```

## 🚀 Step 2: Deploy to Vercel

### 1. Push to GitHub:
```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Prepare for Vercel deployment"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/django-it-helpdesk.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Vercel:
1. Go to https://vercel.com and sign up/login
2. Click **"New Project"**
3. Import your GitHub repository
4. **Framework Preset:** Other
5. **Build Command:** `chmod +x build_files.sh && ./build_files.sh`
6. **Output Directory:** `staticfiles_build`
7. Click **"Deploy"**

### 3. Configure Environment Variables:
1. In Vercel dashboard, go to your project
2. **Settings** → **Environment Variables**
3. Add all variables from your `.env` file:
   ```
   DJANGO_SECRET_KEY=your-secret-key
   DJANGO_SETTINGS_MODULE=helpdesk.settings_vercel
   DB_NAME=your-database-name
   DB_USER=your-database-user
   DB_PASSWORD=your-database-password
   DB_HOST=your-database-host
   DB_PORT=3306
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=abbakariamali@gmail.com
   EMAIL_HOST_PASSWORD=fjikqzmjqcfqhhfc
   DEFAULT_FROM_EMAIL=superdoll.co.tz
   ```

### 4. Add Custom Domain:
1. In Vercel dashboard → **Settings** → **Domains**
2. Add `superdoll.co.tz` and `www.superdoll.co.tz`
3. Configure DNS records as shown by Vercel
4. SSL certificate will be automatically generated

## 📊 Database Options for Vercel:

### Option A: PlanetScale (Recommended)
- MySQL-compatible serverless database
- Free tier available
- Automatic scaling

### Option B: Railway MySQL
- Traditional MySQL hosting
- Easy setup
- Affordable pricing

### Option C: Keep XAMPP (Development Only)
- Use for development
- Deploy with cloud database for production

## 🔧 Limitations & Considerations:

### Vercel Limitations:
- **Serverless functions** (no persistent connections)
- **No WebSocket support** (Channels won't work)
- **10-second execution limit** per request
- **File uploads** need external storage (AWS S3, Cloudinary)

### Solutions:
- Use **Pusher** or **Ably** for real-time features instead of Channels
- Use **Cloudinary** or **AWS S3** for media file storage
- Optimize database queries for serverless environment

## 🎉 Benefits:
- ✅ **Zero server management**
- ✅ **Automatic SSL & CDN**
- ✅ **Global edge deployment**
- ✅ **Automatic scaling**
- ✅ **Git-based deployments**
- ✅ **Free tier available**
