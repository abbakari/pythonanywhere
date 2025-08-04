import os
from django.core.wsgi import get_wsgi_application

# Set the settings module - use environment variable or default to production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings_production')

# Get the WSGI application
application = get_wsgi_application()
