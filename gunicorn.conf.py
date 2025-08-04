"""
Gunicorn configuration for Django IT Helpdesk production deployment.
"""

import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = "info"

# Process naming
proc_name = 'django_it_helpdesk'

# Server mechanics
daemon = False
pidfile = 'logs/gunicorn.pid'
user = None
group = None
tmp_upload_dir = None

# SSL (uncomment when using HTTPS)
# keyfile = "/path/to/your/ssl/key.pem"
# certfile = "/path/to/your/ssl/cert.pem"
