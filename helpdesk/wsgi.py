import os
from django.core.wsgi import get_wsgi_application

# Set the settings module for Vercel deployment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings_vercel')

# Get the WSGI application
application = get_wsgi_application()

# Vercel serverless function handler
app = application
